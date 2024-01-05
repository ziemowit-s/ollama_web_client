# Ollama Client Setup

## Prerequisites

### Install and Run Ollama
First, install Ollama using the provided script. This will set up the necessary environment on your system.

```bash
curl https://ollama.ai/install.sh | sh
```

Download the desired model (for example, `llama2`):

```bash
ollama pull llama2
```

### Create a HTTPS Certificate
For local development, create a self-signed SSL certificate:

1. Generate a new private key and certificate signing request:

   ```bash
   openssl req -newkey rsa:2048 -nodes -keyout domain.key -out domain.csr
   ```

   Answer the prompts for the certificate signing request.

2. Generate a self-signed SSL certificate:

   ```bash
   openssl x509 -signkey domain.key -in domain.csr -req -days 365 -out domain.crt
   ```

   This process will create `domain.key` (your private key) and `domain.crt` (your self-signed certificate).

   **Note**: Self-signed certificates will trigger browser warnings but are acceptable for local development.

## Running the Services

### Start the Ollama Server
Run the Ollama server to serve the models.

```bash
ollama serve
```

### Start the Python Client Server
Run the Python server which interfaces with the Ollama server and serves the web client.

```bash
python server.py
```

### Accessing the Web Client
Open a web browser and navigate to the server's IP address at the specified port. For example:
https://192.168.194.101:4443


**Note**: There might be a security warning due to the self-signed certificate. This is expected and can be bypassed in a development environment.

