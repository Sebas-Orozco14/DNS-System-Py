from modulos import *


class myHandler(BaseRequestHandler):    #Se define la clase myHandler para manejar el servidor local
   def handle(self):
       print("Command channel established")
       print ("Connection from ", str(self.client_address))     #Se conectan los clientes y se muestra el extremo de la conexion
       self.request.send("Welcome, How can I help you? ".encode())
       while True:
           data = self.request.recv(1024)      #Se espera recibir el mensaje del cliente de la forma <dominio> <tipo> <port>
           if data.decode() == "QUIT":
               print("Command Channel closed")   #Si el mensaje es QUIT es el comando para cerrar el canal de control
               break
           else:
               fin_url = data.decode().index(" ")   #Se busca separar el mensaje <dominio> <tipo> del <puerto> para redireccionar la peticion
               dominio = data.decode()[:fin_url]
               new_data = data.decode()[fin_url+1:]
               find_port = new_data.index(" ")
               port = new_data[find_port+1:]    #Se extrae el puerto que el cliente tiene en escucha para el canal de datos
               msg = data.decode()[:find_port+fin_url+1]    #Mensaje con el dominio y el puerto
               s_d = socket(AF_INET,SOCK_STREAM)    #Se crea el socket para el canal de datos
               s_d.connect((str(self.client_address)[2:12],int(port)))   #Se conecta el socket al extremo del canal de datos
               print("Data channel established with (",str(self.client_address),int(port),")")
               ###
               if dominio[-3:] == "edu":     #Si el dominio termina en edu se redirecciona al servidor de zona EDU
                   s_udp = socket(AF_INET,SOCK_DGRAM)    #Se crea el socket para la conexion UDP con el servidor de zona
                   print("Retransmitting request")
                   s_udp.sendto(msg.encode(),("172.17.0.3",53))   #Se conecta y se redirecciona la peticion al puerto 53 del servidor edu
                   data, remote_host = s_udp.recvfrom(1024)     #Recibe la respuesta a la peticion
                   cifrado = cifrar_cesar(data.decode(),5)    #Se encripta la respuesta del servidor de zona para enviarla al cliente
                   print("Sending reply")
                   s_d.send(cifrado.encode())     #Se envia la respuesta cifrada por el canal de datos
               elif dominio[-3:] == "net":    #Si el dominio termina en net se redirecciona al servidor de zona NET
                   s_udp = socket(AF_INET,SOCK_DGRAM)
                   print("Retransmitting request")
                   s_udp.sendto(msg.encode(),("172.17.0.4",53))  #Se conecta y se redirecciona la peticion al puerto 53 del servidor net
                   data, remote_host = s_udp.recvfrom(1024)
                   cifrado = cifrar_cesar(data.decode(),5)
                   print("Sending reply")
                   s_d.send(cifrado.encode())
               else:
                   s_d.send("This type of domain cannot be find here".encode())  #Si la peticion es de un dominio distinto de net o edu se rechaza la peticion
               ###
               print("Data channel closed")
               s_d.close()


myServer = ForkingTCPServer(("172.17.0.2", 5353), myHandler)   #Se usa Forking para poder atender varios clientes "simultaneamente"
print("Waiting connection...")
myServer.serve_forever()
