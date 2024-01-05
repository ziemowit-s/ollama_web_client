# Prerequisites
Install Ollama:
```bash
curl https://ollama.ai/install.sh | sh
```

Download the model
```bash
ollama pull llama2
```

# Run
Start the Ollama server
```bash
ollama serve
```

Start the python client server
```bash
server.py
```

enter the website (IP address of NeuroinflabD):
https://192.168.194.101:4443

# Create a HTTPS certificate
To create a self-signed SSL certificate for local development on Ubuntu 22.04, you can use the openssl command. Here are the steps to create a self-signed certificate:Open a terminal and use the following command to generate a new private key and certificate signing request:

    bash

    openssl req -newkey rsa:2048 -nodes -keyout domain.key -out domain.csr

Answer the questions for the certificate signing request. Since this is for development, you can use your localhost information or leave them blank. Generate a self-signed SSL certificate with the following command:

    bash

    openssl x509 -signkey domain.key -in domain.csr -req -days 365 -out domain.crt

    You now have domain.key (your private key) and domain.crt (your self-signed certificate) that you can use in your server configuration.

Remember that self-signed certificates will trigger warnings in browsers because they aren't signed by a recognized certificate authority. However, for local development, you can safely proceed past the warning.