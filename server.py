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
        print "El cliente " + str(self.client_address) + " nos manda:"
        # Escribe dirección y puerto del cliente (de tupla client_address)
        User = ""
        while 1:
            # Leyendo mensaje a mensaje lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            else:
                print line
                WordList = line.split(' ')
                User = WordList[1].split(':')[1]
                DiccUsers[User] = self.client_address[0]
                #Lo añadimos al diccionario de usuarios
                Time = int(WordList[3])
                if Time == 0:
                    del DiccUsers[User]
                    #Lo eliminamos del diccionario
                print "Enviando: SIP/1.0 200 OK"
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
            

if __name__ == "__main__":
    DiccUsers = {}  # Creo el diccionario de usuarios e IPs
    listarg = sys.argv
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(listarg[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
