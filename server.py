#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
   
    diccionario={}
    
    def procesarmensaje(self,line):
        mensaje = line.split(" ")
        
        if mensaje[0] == "REGISTER":
            direccion= mensaje[1].split(":")
            lista=[self.client_address[0],time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))]
            self.diccionario[direccion[-1]]= lista
            self.wfile.write("SIP/2.0 200 OK" + '\r\n' + '\r\n')
            print "El cliente nos manda " + line
            self.resgister2file()
            if int(mensaje[-1]) == 0:
                del self.diccionario[direccion[-1]]
                self.wfile.write("SIP/2.0 200 OK" + '\r\n' + '\r\n')

    def resgister2file(self):
        fich = open("registered.txt", "w")
        claves=self.diccionario.keys()
        for i in claves:
           linea= i + '\t' + self.diccionario[i][0] + '\t' + self.diccionario[i][1]
           fich.write(linea)

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\r\n')
       
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            print self.client_address[0] + " " + str(self.client_address[1])
            line = self.rfile.read()
            self.procesarmensaje(line)
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    HOST,PORT="",int(sys.argv[1])
    serv = SocketServer.UDPServer((HOST,PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
