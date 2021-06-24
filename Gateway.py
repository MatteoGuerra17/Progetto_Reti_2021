# -*- coding: utf-8 -*-
"""
@author: Matteo Guerra
matricola: 924497
"""

import socket as sk
import time as t
import sys

# Creo il socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
  
count = 4 #contatore che serve se tutti i device hanno mandato le loro misure
misure=[] #lista in cui metto le misure
indirizzo=[] #lista in cui metto gli indirizzi

# Associo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    if(count == 0):
        print('ricevute tutte le misure dai 4 dispositivi') 
        break #quando count è 0 significa che più nessun device deve inviare le misure quindi esco dal while
        
    print('\n\r waiting to receive message from devices...')
    
    #ricevo le misure
    data, address = sock.recvfrom(4096)
    misure.append(data) #metto le misure nella lista
    indirizzo.append(address) #metto gli indirizzi nella lista    
    
    print('received data from {}'.format(address)) #stampo l'indirizzo dal quale ho ricevuto le misure
    print (data.decode('utf8')) #stampo le misure ricevute
    count -= 1 #decremento count perchè significa che ho ricevuto le misure

    if data:
        #dico al device che ho ottenuto le misure correttamente
        data1 = 'Misure ricevute'
        sent = sock.sendto(data1.encode(), address)
        print ('sent %s bytes back to %s' % (sent, address))
        
sock.close() #quando ricevo tutte le misure chiudo il socket e dopo 10 sec apro la connessione TCP col Cloud
t.sleep(10)
        
#socket TCP verso il cloud
clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

#indirizzo
server_address = ('localhost', 8080)
host, port = server_address

try:
    clientsocket.connect((host,port)) #connetto il socket a quel indirizzo
except Exception as e:
    print (Exception,":",e)
    print ("Connessione andata male. Riprova\r\n")
    sys.exit(0)

risp=[] #lista per mettere le risposte ricevute dal Cloud
start = t.time() #faccio partire il tempo per capire quanto impiega un pacchetto TCP
for i in range(0,4):
    clientsocket.send(misure[i]) #invio al Cloud le misure
    t.sleep(5) #aspetto 5 sec
    response = clientsocket.recv(1024) #ricevo la risposta da parte del Cloud
    risp.append(response) #appendo la riposta in coda alla lista
end = t.time() #stoppo il tempo

print("tempo per inviare il pacchetto TCP: {} sec".format(end-start-20)) #stampo il tempo impiegato
#tolgo 20 sec perchè nel ciclo for precedente aspetto 5 secondi tra l'invio delle misure e la ricezione delle risposte
#e siccome lo eseguo per 4 volte: 5 sec x 4 volte = 20 sec da togliere

for i in range(0,4):
    print(risp[i]) #infine stampo tutte le risposte


clientsocket.close() #chiudo il socket