
import http.server
import cgi

import json
from base64 import b64encode

class ServerHandler(http.server.SimpleHTTPRequestHandler): 

    def _load_credentials(self):
        # Load the admin credentials from the
        # json file and encode in b64 for base auth

        with open('data/credentials.json') as data:
            jsondata = json.load(data)
            self.credentials = f'{jsondata["username"]}:{jsondata["password"]}'
            self.credentials = 'Basic ' + b64encode(
                self.credentials.encode()).decode("ascii")
        return self.credentials

    #Mando un errore 401 e richiedo le credenziali
    def auth_required(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("pages/Auth_required.html", 'rb') as file:
            self._data = file.read()

        self.wfile.write(self._data)

    def do_GET(self):
        #Controllo se l'utente chiede una pagina protetta
        if self.path  == "/data/Request.html":
            #Controllo se le credenziali sono state inizializzate, in caso negativo le inizializzo
            if not hasattr(self, 'credentials'):
                self._load_credentials()
        
            if self.headers.get("Authorization") == None:
                self.auth_required()

            elif self.headers.get("Authorization") != self.credentials:
                self.auth_required()
            
            elif self.headers.get("Authorization") == self.credentials:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                http.server.SimpleHTTPRequestHandler.do_GET(self)


        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)


        
    def do_POST(self):
        try:
            # Salvo i vari dati inseriti
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
            
            # Con getvalue prendo i dati inseriti dall'utente
            name = form.getvalue('name')
            email = form.getvalue('email')
            numero = form.getvalue('numero')

            # Stampo all'utente i dati che ha inviato
            output="<html><body>Richiesta inviata correttamente, verrai contattato dal dottore per l'appuntamento<br><br>NOME e COGNOME: " + name + "<br>E-MAIL: " + email + "<br>NUMERO: " + numero +"<br><br><a href='/index.html'>Torna alla Home</a></body></html>"
            self.send_response(200)
        except: 
            self.send_error(404, 'Bad request submitted.')
            return
        
        self.end_headers()
        self.wfile.write(bytes(output, 'utf-8'))
        
        # Salvo in locale i vari messaggi in AllPOST
        with open("data/Request.html", "a") as out:
          info = "<p>NOME e COGNOME: " + name + "</p></p>E-MAIL: " + email + "</p><p>NUMEO: "+ numero +"</p><br><br>\n"
          out.write(info)