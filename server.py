#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys





class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        print self.client_address
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            ListaMitad = line.split(':')
            Type = ListaMitad[0].split(' ')[0]
            
            if Type == "REGISTER":
                User = ListaMitad[-1].split(' ')[0]
                DiccUsers[User] = self.client_address[0]
                print DiccUsers
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    DiccUsers = {}  # Creo el diccionario de usuarios e IPs
    listarg = sys.argv
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(listarg[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
