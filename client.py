#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

lista = sys.argv

if len(lista) == 6:
    # Cliente UDP simple.
    # Dirección IP del servidor.
    SERVER = lista[1]
    PORT = int(lista[2])

    # Contenido que vamos a enviar
    LINE = lista[3].upper() + " sip:" + lista[4] + " SIP/2.0 \r\n"
    LINE = LINE + "Expires: " + lista[5] + "\r\n\r\n"

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print "Enviando: " + LINE
    my_socket.send(LINE)
    data = my_socket.recv(1024)

    print 'Recibido -- ', data
    print "Terminando socket..."

    # Cerramos todo
    my_socket.close()
    print "Fin."
else:
    print "Usage: client.py ip puerto register sip_address expires_value"
