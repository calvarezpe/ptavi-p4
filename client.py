#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


listarg = sys.argv

# Cliente UDP simple.

try:


#    Asignamiento de los parámetros introducidos por la línea de comandos
#    a variables globales

    # Dirección IP del servidor.
    SERVER = listarg[1]
    PORT = int(listarg[2])

    # Tipo de contenido que vamos a enviar
    TYPE = listarg[3]

    # Contenido que vamos a enviar
    LINE = listarg[4]

    # Valor de Expires en segundos
    EXPIRES = listarg[5]

except IndexError:
    sys.exit('client.py ip puerto register sip_address expires_value')
except ValueError:
    sys.exit('client.py ip puerto register sip_address expires_value')


#Inicio del protocolo de envío de mensajes al servidor


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + TYPE.upper() + " sip:" + LINE + " SIP/2.0"
print "\t  Expires: " + EXPIRES
my_socket.send(TYPE.upper() + " sip:" + LINE + " SIP/2.0" + "\r\n"
               + "Expires: " + str(EXPIRES) + "\r\n\r\n")
# Mandamos un solo string
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
