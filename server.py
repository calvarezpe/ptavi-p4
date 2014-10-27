#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de SIP
en UDP simple
"""

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    direcciones = {}
    
    def register2file(self):
        fich = open("registered.txt", "w")
        line = "User\tIP\tExpires\r\n"
        for direccion in self.direcciones.keys():
            hora = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.direcciones[direccion][1]))
            line += direccion + "\t" + self.direcciones[direccion][0] + "\t" + hora + "\r\n"
        fich.write(line)
            
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print "El cliente nos manda " + line
            elements = line.split()
            direccion = (elements[1].split(":"))[1];
            expires = elements[-1]
            if expires > "0":
                hora = float(expires) + time.time()
                self.direcciones[direccion] = (self.client_address[0], hora)
                self.wfile.write("SIP/2.0 200 OK \r\n\r\n")
            elif expires == "0":
                if self.direcciones.has_key(direccion):
                    del self.direcciones[direccion]
                    self.wfile.write("SIP/2.0 200 OK \r\n\r\n")
                else:
                    self.wfile.write("SIP/2.0 404 NOT FOUND \r\n\r\n")
            for direccion in self.direcciones.keys():
                if self.direcciones[direccion][1] < time.time():
                    del self.direcciones[direccion]
            self.register2file()
        
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
