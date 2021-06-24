# -*- coding: utf-8 -*-
"""
@author: Matteo Guerra
matricola: 924497
"""

import socket as sk
import time as t

#apro il file dove ho scritto le misure in modalità lettura
FILE = 'misure_dev1.txt'
f = open(FILE, "r")

#imposto l'ip arbitrariamente perchè mi servirà quando andrò a stampare le misure
my_ip='192.168.1.1'
#leggo i dati dal file
dati = f.read()

# Creo il socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

#associo l'indirizzo locale al server
server_address = ('localhost', 10000)

try:

    # invio i dati raccolti al Gateway
    print ('sending data \n"%s"' % dati)
    t.sleep(1) #1 secondo prima di inviargli i dati
    start = t.time() #parte il timer per capire quanto ci impiega ad arrivare un pacchetto UDP
    sent = sock.sendto(dati.encode(),server_address)
    
    # Ricevo la risposta dal Gateway    
    print('waiting to receive response from')
    data, server = sock.recvfrom(1024)
    end = t.time()
    
    t.sleep(1) #aspetto un secondo e stampo la risposta ricevuta dal Gateway
    print('received message "%s"' % data.decode('utf8'))
    #stampo il tempo impiegato dal pacchetto UDP
    print("tempo per inviare il pacchetto UDP: {} sec".format(end-start)) #stampo il tempo che ci ha impiegato un pacchetto UDP
    
except Exception as info:
    print(info)
finally:
    print ('closing socket')
    #chiudo il socket e il file
    sock.close()
    f.close()

