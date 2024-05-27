from modulos import *


class myTCPHandler(BaseRequestHandler):     #Conexion TCP para los Admin de zona
   global DB
   DB = []  #base de datos de objetos tipo dominio
   def handle(self):
       print ("TCP Connection from ", str(self.client_address))
       while True:
           data = self.request.recv(1024)
           if data.decode() == "QUIT": break    #Comando para salir de la sesion
           elif data.decode() == "REGI":         #Comando para registrar una nueva entrada en la DB
               print("Registering domain")
               data2 = self.request.recv(1024)
               list_rx = pickle.loads(data2)      #Pasa de serial al formato de lista la lista enviada
               register = Dominio(list_rx[0],list_rx[1],list_rx[2],list_rx[3])   #Crea el objeto Dominio con los datos enviados
               DB.append(register)       #Almacena en la DB el objeto creado
           elif data.decode() == "DELE":      #Comando para eliminar un registro de la DB
               print("Deleting domain")
               data2 = self.request.recv(1024)
               for entry in range(len(DB)):
                   if data2.decode() == DB[entry].URL:    #Si el nombre de dominio de la posicion i en la DB coincide con el dominio requerido para eliminar
                       DB.pop(entry)     #Eliminar el registro
           elif data.decode() == "LIST":
               self.request.send(str(len(DB)).encode())     #Envia la cantidad de registros que tiene actualmente la DB
               print("Listing domains")
               if len(DB) != 0:
                   ack = self.request.recv(1024)      #Recibe un ACK del Admin para poder realizar los envios de los registros
                   for i in range(len(DB)):
                       list = pickle.dumps(DB[i])     #Serializa el objeto Dominio de la pisicion i de la DB
                       self.request.send(list)        #Envia el objeto serializado
                       ack = self.request.recv(1024)   #Recibe un ACK del Admin al recibir el objeto
       self.request.close()


class myUDPHandler(BaseRequestHandler):    #Conexion UDP para las peticiones del DNS local
   def handle(self):
       print ("UDP Connection from ", str(self.client_address))
       data, conn = self.request
       flag = 0    #Bandera para verificar si se encuentra el nombre de dominio en la DB
       fin_url = data.decode().index(" ")   #Se busca la posicion donde finaliza el nombre de dominio
       url = data.decode()[0:fin_url]      #Saca el nombre de dominio del string que recibio
       registro = data.decode()[fin_url+1:]  #Se saca el tipo de registro requerido por el cliente del mensaje recibido
       for entry in range(len(DB)):
           if url == DB[entry].URL:    #Si el nombre de dominio esta registrado en la DB
               flag = 1
               if registro == "IPV4":     #Verifica que registro se solicito para extraerlo de la DB
                   tipo = DB[entry].IPV4
               elif registro == "IPV6":
                   tipo = DB[entry].IPV6
               elif registro == "TXT":
                   tipo = DB[entry].TXT
               else:
                   tipo = "Invalid Type"
       if flag == 0:
           tipo = "Not found the URL"
       print("Sendind register")
       conn.sendto(tipo.encode(),self.client_address)   #Envia el registro solicitado


myTCPServer = ThreadingTCPServer(("172.17.0.3", 53535), myTCPHandler)    #IP del contenedor del servidor
myUDPServer = ThreadingUDPServer(("172.17.0.3", 53), myUDPHandler)


hilo_tcp = Thread(target=myTCPServer.serve_forever)
hilo_udp = Thread(target=myUDPServer.serve_forever)


hilo_tcp.start()
hilo_udp.start()
