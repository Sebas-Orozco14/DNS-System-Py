from modulos import *
c_c = socket(AF_INET,SOCK_STREAM)  #Socket del puerto de control
c_c.connect(("172.17.0.2",5353))   #Se conecta al extremo del servidor local
print("Command channel established") 
data = c_c.recv(1024)
print (data.decode())
while True:
   request=input("Request> ")
   c_c.send(request.encode())
   if request == "QUIT":   #Comando para salir
       break
   else:
       fin_url = request.index(" ")
       new_data = request[fin_url+1:]
       find_port = new_data.index(" ")
       port = new_data[find_port+1:]   #Se extrae del request el puerto indicado para el canal de datos
       host = c_c.getsockname()[0]   #Saca la IP del socket de origen del canal de datos para poder abrir el puerto del canal de datos
       c_d = socket(AF_INET,SOCK_STREAM)  #Socket del puerto de datos
       c_d.bind((str(host),int(port))) 
       c_d.listen(5)    #se pone en escucha el puerto de datos ya que es el que recibe la info
       conn, add = c_d.accept()     #acepta la conexion del servidor por el canal de datos
       print("Data channel established with", add)
       msg1 = conn.recv(1024)    #Recibe el mensaje encriptado que le envia el servidor local
       print("Encrypted message:")
       print(msg1.decode())
       descifrado = descifrar_cesar(msg1.decode(),5)   #Desencripta el mensaje
       print("Decrypted message:")
       print(descifrado)
       print("Data channel closed")
       conn.close()     #cierra el canal de datos
       c_d.close()


print("Command Channel closed")
c_c.close()
