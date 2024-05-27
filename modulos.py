from socketserver import ForkingTCPServer, ThreadingTCPServer, ThreadingUDPServer, BaseRequestHandler
from threading import Thread
import pickle
from socket import *


class Dominio:
   "Domain Register"
   def __init__(self,URL,IPV4,IPV6,TXT):   #Atributos: vnombre de dominio, direccion ipv4, direccion ipv6 y descripcion general
       self.URL = URL
       self.IPV4 = IPV4
       self.IPV6 = IPV6
       self.TXT = TXT
   def __str__(self):
       return (self.URL, self.IPV4, self.IPV6, self.TXT)   #Funcion para enseñar los atributos


def cifrar_cesar(texto, clave):   #Funcion para cifrado tipo cesar
   resultado = ""
   for caracter in texto:
       if caracter.isalpha():     #detecta si el caracter actual es del alfabeto (True) o es otro caracter (False)
           if caracter.isupper(): 
               resultado += chr((ord(caracter) - 65 + clave) % 26 + 65)   #Si la letra esta en mayuscula le resta el 65 que es el cinjunto ASCII de las mayusculas
           else:
               resultado += chr((ord(caracter) - 97 + clave) % 26 + 97)   #Si la letra es minuscula le resta 97 que es el conjunto ASCII de las minusculas
       elif caracter.isdigit():     #detecta si el caracter actual es un numero
           resultado += str((int(caracter) + clave) % 10)     #se le suma la clave y se verifica que este dentro de los digitos del 0 al 9 con el modulo %10
       elif caracter == ".":
           resultado += caracter    #si el caracter es un "." se deja sin modificar
       else:
           resultado += chr((ord(caracter) + clave) % 256)   #si es un caracter especial se le suma la clave y se verifica que este dentro del codigo ASCII (256 caracteres)
   return resultado


def descifrar_cesar(texto_cifrado, clave):
   return cifrar_cesar(texto_cifrado, -clave)   #Revierte la funcion cifrar_cesar
