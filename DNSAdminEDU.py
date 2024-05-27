from modulos import *


a = socket(AF_INET,SOCK_STREAM)  #Se crea el socket TCP
a.connect(("172.17.0.3",53535))   #Se conecta al puerto 53535 del DNS edu
print("Welcome Admin! Please type the request that you want to do [REGI] to resgister, [DELE] to delete, [LIST] to see the actual DB")


while True:
   request = input("Request> ")
   a.send(request.encode())
   if request == "REGI":
       list = []   #Lista para ingresar los registros asociados a un dominio
       request2 = input("Register [Domain_name]> ")
       list.append(request2)
       request2 = input("Register [IPV4] > ")
       list.append(request2)
       request2 = input("Register [IPV6] > ")
       list.append(request2)
       request2 = input("Register [TXT] > ")
       list.append(request2)
       list_tx = pickle.dumps(list)   #Se serializa la lista para poderla enviar al servidor de zona
       a.send(list_tx)    #Se envia al servidor de zona
   elif request == "DELE":
       request2 = input("Delete  [Domain_name] > ")
       a.send(request2.encode())   #Se envia el dominio a eliminar al servidor de zona
   elif request == "LIST":
       list = []
       data = a.recv(1024)
       if data.decode() == "0":    #Si el tamaño de la lista actual es 0 significa que no hay registros
           print("There is no Registers in DNS Zone")
       else:
           a.send("OK".encode())   #Se envia un ACK para poder recibir los objetos que envia el servidor de zona
           for i in range(int(data.decode())):
               data_rx = a.recv(4092)
               data_var = pickle.loads(data_rx)    #Carga los datos serializados del objeto tipo Dominio
               list.append(data_var)          #Ingresa los objetos a una lista
               a.send("OK".encode())      #Envia un ACK para que el servidor envie el siguiente objeto de la DB
           print("Actual Data Base of DNS Zone: ")
           for i in range(len(list)):
               print(list[i].__str__())    #Muestra los objetos que se ingresaron a la lista y con la funcion __str__ muestra sus atributos (registros)
   elif request == "QUIT":    #Comando para salir
       break
   else:
       print("Not valid command!")


print("Good bye Admin! See you soon")
a.close()
