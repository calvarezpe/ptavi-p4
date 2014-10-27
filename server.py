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
    SIPRegister server class
    """
   
    diccionario={}
    
    def procesarmensaje(self,line):
        """
        Save and delete users
        
        Keyword arguments:
        
        line -- client message
        """
        mensaje = line.split(" ")
        fecha_entrada=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        hora_actual=time.mktime(time.strptime(fecha_entrada,'%Y-%m-%d %H:%M:%S'))
        if mensaje[0] == "REGISTER":
            direccion= mensaje[1].split(":")
            expires=mensaje[-1]
            lista=[self.client_address[0],time.strftime(fecha_entrada),expires]
            self.diccionario[direccion[-1]]= lista
            self.wfile.write("SIP/2.0 200 OK" + '\r\n' + '\r\n')
            print "El cliente nos manda " + line
            if int(expires) == 0:
                del self.diccionario[direccion[-1]]
                self.wfile.write("SIP/2.0 200 OK" + '\r\n' + '\r\n')
            self.caducidad(hora_actual)
        self.register2file()
        
    def caducidad(self, hora_actual):
        """
        delete expired users
        """   
            
        claves=self.diccionario.keys()
        for i in claves:
            hora_entrada=time.strptime(self.diccionario[i][1],'%Y-%m-%d %H:%M:%S')
            hora_expiracion=time.mktime(hora_entrada) + float(self.diccionario[i][2])
            if hora_actual > hora_expiracion:
                del self.diccionario[i]
        

    def register2file(self):
        """
        create users file
        """
        fich = open("registered.txt", "w")
        claves=self.diccionario.keys()
        for i in claves:
           linea= i + '\t' + self.diccionario[i][0] + '\t' + self.diccionario[i][1] +'\r\n'
           fich.write(linea)

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\r\n')
        print "IP: " + self.client_address[0] + " " + "PORT: " + str(self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
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
