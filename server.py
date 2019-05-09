import http.server
import socketserver
import requests

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000

import requests


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    # GET
    def do_GET(self):
        #Send response status code
        self.send_response(200)

        #Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        if self.path == "/":
            #self.send_response(200)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            filename = "index.html"
            print("File to send: {}".format(filename))
            with open(filename, "r") as f:
                content = f.read()
                # Write content as utf-8 data
                self.wfile.write(bytes(content, "utf8"))
                print("File served!")

        elif self.path.startswith('/searchDrug'):
            #self.send_response(200)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            print(self.path)
            path = self.path
            datos = path.split("?")
            active_ingredient = datos[1].split('=')
            active_ingredient = active_ingredient[1]
            print(active_ingredient)
            url=str("https://api.fda.gov/drug/label.json?search=active_ingredient:"+ active_ingredient +"&limit=10")
            data=requests.get(url).json()
            cabecera="""
            <!DOCTYPE html>
            <html>
            <body>

            <ul style="list-style-type:square;">
            """
            cierre="""
            </ul>
            </body>
            </html>
            """
            lista = []
            for result in data['results']:
                try:
                    one=result['openfda']
                    two=one['generic_name']
                    lista.append(str(two))
                except KeyError:
                    lista.append("[Aqui tenemos un medicamento que no contiene el campo generic_name]")
                    print('Este medicamento no tiene el campo generic_name')
            print (lista)
            element=""
            for elem in lista:
                element +=('<li>'+elem+'</li>\n')

            content=cabecera+element+cierre
            print(content)
            self.wfile.write(bytes(content, "utf8"))
            print("File served!")


        elif self.path.startswith('/searchCompany'):
            #self.send_response(200)
            #self.send_header('ContentException-type', 'text/html')
            #self.end_headers()
            print(self.path)
            path = self.path
            datos = path.split("?")
            company = datos[1].split('=')[1]
            print(company)
            url=str("https://api.fda.gov/drug/label.json?search=openfda.manufacturer_name:"+ company +"&limit=10")
            data=requests.get(url).json()
            cabecera="""
            <!DOCTYPE html>
            <html>
            <body>

            <ul style="list-style-type:square;">
            """
            cierre="""
            </ul>
            </body>
            </html>
            """

            lista2 = []
            for result in data['results']:
                try:
                    one=result['openfda']
                    two=one['manufacturer_name']
                    lista2.append(str(two))
                except KeyError:
                    lista2.append("[No se encontró el campo manufacturer_name]")
                    print('No existe resultado para esa búsqueda')
            print(lista2)
            element=""
            for elem in lista2:
                element +=('<li>'+elem+'</li>\n')

            content=cabecera+element+cierre
            print(content)
            self.wfile.write(bytes(content, "utf8"))
            print("File served!")

        elif self.path.startswith('/listDrugs'):
            #self.send_response(200)
            #self.send_header('ContentException-type', 'text/html')
            #self.end_headers()
            print(self.path)
            path = self.path
            datos = path.split("?")
            respuesta = datos[1].split('=')
            respuesta = respuesta[1]
            if respuesta == 'yes':
                url="https://api.fda.gov/drug/ndc.json?count=generic_name.exact&limit=10"
                data=requests.get(url).json()
                cabecera="""
                <!DOCTYPE html>
                <html>
                <body>

                <ul style="list-style-type:square;">
                """
                cierre="""
                </ul>
                </body>
                </html>
                """
                lista3=[]
                for result in data['results']:
                    try:
                        one=result['term']
                        lista3.append(one)
                    except KeyError:
                        lista3.append('<li>'+'No existe resultado para esa búsqueda'+'<li>')
                        print('No existe resultado para esa búsqueda')
                print(lista3)
                element=""
                for elem in lista3:
                    element +=('<li>'+elem+'</li>\n')

                content=cabecera+element+cierre
                print(content)
                self.wfile.write(bytes(content, "utf8"))
                print("File served!")
            else:
                filename = "index.html"
                print("File to send: {}".format(filename))
                with open(filename, "r") as f:
                    content = f.read()
                    # Write content as utf-8 data
                    self.wfile.write(bytes(content, "utf8"))
                    print("File served!")




        elif self.path.startswith('/listCompanies'):
            #self.send_response(200)
            #self.send_header('ContentException-type', 'text/html')
            #self.end_headers()
            print(self.path)
            path = self.path
            datos = path.split("?")
            respuesta = datos[1].split('=')
            respuesta = respuesta[1]
            if respuesta == 'yes':
                url="https://api.fda.gov/drug/ndc.json?count=openfda.manufacturer_name.exact&limit=10"
                data=requests.get(url)
                data = data.json()
                cabecera="""
                <!DOCTYPE html>
                <html>
                <body>

                <ul style="list-style-type:square;">
                """
                cierre="""
                </ul>
                </body>
                </html>
                """
                lista4=[]
                for result in data['results']:
                    try:
                        one=result['term']
                        lista4.append(one)
                    except KeyError:
                        lista4.append('<li>'+'No existe resultado para esa búsqueda'+'<li>')
                        print('No existe resultado para esa búsqueda')
                print(lista4)
                element=""
                for elem in lista4:
                    element +=('<li>'+elem+'</li>\n')

                content=cabecera+element+cierre
                print(content)
                self.wfile.write(bytes(content, "utf8"))
                print("File served!")
            else:
                #self.send_response(200)
                #self.send_header('ContentException-type', 'text/html')
                #self.end_headers()
                filename = "index.html"
                print("File to send: {}".format(filename))
                with open(filename, "r") as f:
                    content = f.read()
                    # Write content as utf-8 data
                    self.wfile.write(bytes(content, "utf8"))
                    print("File served!")

        elif self.path == "/listWarnings":
            url="https://api.fda.gov/drug/label.json?search=warnings&limit=10"
            data=requests.get(url)
            data = data.json()
            cabecera="""
            <!DOCTYPE html>
            <html>
            <body>

            <ul style="list-style-type:square;">
            """
            cierre="""
            </ul>
            </body>
            </html>
            """
            advertencias =[]
            for result in data['results']:
                try:
                    one=result['warnings']
                    advertencias.append(one)
                except KeyError:
                    advertencias.append('<li>'+'No existe resultado para esa búsqueda'+'<li>')
                    print('No existe resultado para esa búsqueda')
            print(advertencias)
            warnings=""
            for elem in advertencias:
                warnings +=('<li>'+str(elem)+'</li>\n')

            content=cabecera+warnings+cierre
            print(content)
            self.wfile.write(bytes(content, "utf8"))
            print("File served!")


        elif self.path == "/favicon.ico":
            print("Conexión con favicon.ico")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            filename = "error.html"
            print("File to send: {}".format(filename))
            with open(filename, "r") as f:
                content = f.read()
            # Write content as utf-8 data
            self.wfile.write(bytes(content, "utf8"))
            print("File served!")







        return


Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
socketserver.TCPServer.allow_reuse_address = True
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
