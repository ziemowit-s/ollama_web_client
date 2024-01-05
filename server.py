import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests

OLLAMA_ADDRESS = "localhost"
OLLAMA_PORT = 11434


def get_address(path):
    if path.startswith("/"):
        path = path[1:]
    return f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}/{path}"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the path is the root path
        if self.path == '/':
            # Serve index.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())

        # Serve CSS files
        elif self.path.endswith(".css"):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(self.path[1:], 'rb') as file:  # path[1:] to remove the leading '/'
                self.wfile.write(file.read())

        # Serve JavaScript files
        elif self.path.endswith(".js"):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open(self.path[1:], 'rb') as file:
                self.wfile.write(file.read())

        elif self.path == '/models':
            # Fetch model list from local Ollama server
            response = requests.get(get_address(path="api/tags"))
            model_list = [model["name"] for model in response.json()["models"]]
            # Send response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(model_list).encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        # Parse the URL to get the path
        path = urlparse(self.path).path

        if path == "/generate":
            # Read the length of the body
            content_length = int(self.headers['Content-Length'])
            # Read the body itself
            body = self.rfile.read(content_length).decode("utf-8")
            # Convert the body to a Python dictionary
            body_dict = json.loads(body)

            # Make a request to the Ollama server
            response = requests.post(get_address(path="api/generate"), json=body_dict)
            ollama_response = response.json()

            # Send response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ollama_response).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, addr='0.0.0.0', port=4443):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    # Wrap the socket with SSL
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile='domain.key',  # Corrected path to your key file
        certfile='domain.crt',   # Path to your certificate file
        server_side=True
    )

    print(f'Starting https server on {addr}:{port}')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
