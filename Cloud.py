# -*- coding: utf-8 -*-
"""
@author: Matteo Guerra
matricola: 924497
"""

import socket as sk

#creo il socket TCP e associo l'indirizzo
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server_address=('localhost',8080)
serverSocket.bind(server_address)

#tupla con gli indirizzi dei device
address_dev = ('192.168.1.1','192.168.1.2','192.168.1.3','192.168.1.4' )

#Definisce la lunghezza della coda di backlog, ovvero il numero di connessioni in entrata
serverSocket.listen(1)
print ('the web server is up on port:',8080)

while True:

    print ('Ready to serve...')
    #il socket accetta la connessione
    connectionSocket, addr = serverSocket.accept()
    print(connectionSocket,addr)
    
    i=1 #i mi servirà per ciclo e per stampare l'indirizzo corrispondente al device
    while i<5:
        
        try:
            #ricevo il messaggio e lo decodifico in UTF-8
            message = connectionSocket.recv(4096)
            message = message.decode('utf-8')
            if message: 
                #divido le misure ricevute in base allo spazio
                mess_vect = message.split()
                ora,temp,umi = mess_vect[1].split(',') #suddivido la prima misura in base alla virgola e ricavo ora, temperatura e umidità
                ora_1,temp_1,umi_1 = mess_vect[2].split(',') #stessa cosa con la seconda misura
                #stampo le misure
                print ('{}_device_{} - {} - {} - {}'.format(address_dev[i-1],i,ora,temp,umi))
                print ('{}_device_{} - {} - {} - {}'.format(address_dev[i-1],i,ora_1,temp_1,umi_1))
                i+=1
            
            #Invio messaggio OK
            connectionSocket.send("200 OK".encode())                

        except IOError:
            #Invia messaggio di risposta nel caso non abbia ricevuto correttamente le misure
            connectionSocket.send(bytes("misure non ricevute correttamente","UTF-8"))
            connectionSocket.close()

