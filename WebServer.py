#%%

import sys, signal
import http.server
import socketserver

port = 8080

from handler import ServerHandler

server = socketserver.ThreadingTCPServer(('',port), ServerHandler )

#Assicura che da tastiera usando la combinazione
#di tasti Ctrl-C termini in modo pulito tutti i thread generati
server.daemon_threads = True  
#il Server acconsente al riutilizzo del socket anche se ancora non è stato
#rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  

def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# entra nel loop infinito
try:
  while True:
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()
# %%
