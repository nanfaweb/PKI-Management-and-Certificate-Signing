import http.server
import ssl

# Define server address and port
HOST = "localhost"
PORT = 8443

# Define file paths to your certificates
CERTFILE = "nuces.crt"  # Certificate signed by EasyRSA CA
KEYFILE = "nuces.key"   # Server private key


class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        response = """
        <!DOCTYPE html>
        <html>
        <head><title>PKI Demonstration</title></head>
        <body>
            <h1>TLS Handshake Successful!</h1>
            <p>Your client successfully validated this server's X.509 certificate against the Root CA.</p>
        </body>
        </html>
        """
        self.wfile.write(response.encode("utf-8"))


def run_server():
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, SimpleHandler)

    # Configure SSL/TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    # Wrap the socket with TLS
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"HTTPS Server running on https://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    run_server()