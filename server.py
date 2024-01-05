from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

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
            response = requests.post('http://localhost:11434/api/generate', json=body_dict)
            ollama_response = response.json()

            # Send response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ollama_response).encode('utf-8'))

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
