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
    
    def procesarmensaje(self,line,diccionario):
       mensaje = line.split(" ")
       if mensaje[0] == "REGISTRER":
            direccion= mensaje[1].split(":")
            diccionario[direccion[-1]]= self.client_address[0]
            self.wfile.write("SIP/2.0 200 OK" + '\r\n' + '\r\n')
            

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\r\n')
        self.diccionario={}
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            print self.client_address[0] + " " + str(self.client_address[1])
            line = self.rfile.read()
            self.procesarmensaje(line,self.diccionario)
            print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    HOST,PORT="localhost",int(sys.argv[1])
    serv = SocketServer.UDPServer((HOST,PORT ), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
