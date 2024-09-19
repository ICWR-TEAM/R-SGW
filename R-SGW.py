print(r"""
 /$$$$$$$           /$$$$$$   /$$$$$$  /$$      /$$
| $$__  $$         /$$__  $$ /$$__  $$| $$  /$ | $$
| $$  \ $$        | $$  \__/| $$  \__/| $$ /$$$| $$
| $$$$$$$/ /$$$$$$|  $$$$$$ | $$ /$$$$| $$/$$ $$ $$
| $$__  $$|______/ \____  $$| $$|_  $$| $$$$_  $$$$
| $$  \ $$         /$$  \ $$| $$  \ $$| $$$/ \  $$$
| $$  | $$        |  $$$$$$/|  $$$$$$/| $$/   \  $$
|__/  |__/         \______/  \______/ |__/     \__/
===================================================
[*] R-SGW - SSL Gateway | Afrizal F.A - R&D ICWR
===================================================
""")

import argparse
import os
import socket
import ssl
from OpenSSL import crypto

class SSLGateway:
    def __init__(self, ssl_host, ssl_port, backend_host, backend_port, ssl_certfile, ssl_keyfile):
        self.ssl_host = ssl_host
        self.ssl_port = ssl_port
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile

    def generate_self_signed_cert(self):
        if not os.path.exists(self.ssl_certfile) or not os.path.exists(self.ssl_keyfile):
            print("Generating SSL Certificate and Key...")
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 2048)

            cert = crypto.X509()
            cert.get_subject().C = "ID"
            cert.get_subject().ST = "Malang"
            cert.get_subject().L = "Malang"
            cert.get_subject().O = "-"
            cert.get_subject().OU = "-"
            cert.get_subject().CN = "-"
            cert.set_serial_number(1000)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60) # 10 Years
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(k)
            cert.sign(k, 'sha256')

            with open(self.ssl_certfile, "wt") as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
            with open(self.ssl_keyfile, "wt") as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
            print(f"SSL Certificate generated: {self.ssl_certfile}, Key: {self.ssl_keyfile}")
        else:
            print("SSL Certificate and Key already exist.")

    def start(self):
        self.generate_self_signed_cert()
        self.create_ssl_gateway()

    def create_ssl_gateway(self):
        gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gateway_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        gateway_socket.bind((self.ssl_host, self.ssl_port))
        gateway_socket.listen(5)
        print(f"SSL Gateway is running on {self.ssl_host}:{self.ssl_port}, forwarding to {self.backend_host}:{self.backend_port}...")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.ssl_certfile, keyfile=self.ssl_keyfile)

        while True:
            client_socket, addr = gateway_socket.accept()
            print(f"SSL Connection from {addr}")

            ssl_client_socket = None
            try:
                ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
                print(f"SSL connection established with {addr}")

                backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                backend_socket.connect((self.backend_host, self.backend_port))
                print(f"Connected to backend {self.backend_host}:{self.backend_port}")

                self.forward_data(ssl_client_socket, backend_socket)

            except ssl.SSLError as e:
                print(f"SSL error: {e}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if ssl_client_socket:
                    ssl_client_socket.close()
                client_socket.close()

    def forward_data(self, client_socket, backend_socket):
        try:
            while True:
                data_from_client = client_socket.recv(4096)
                if not data_from_client:
                    break
                backend_socket.sendall(data_from_client)

                data_from_backend = backend_socket.recv(4096)
                if not data_from_backend:
                    break
                client_socket.sendall(data_from_backend)
        except Exception as e:
            print(f"Error forwarding data: {e}")

def main():
    parser = argparse.ArgumentParser(description='SSL Gateway Configuration.')
    parser.add_argument('--ssl_host', type=str, default='localhost', help='SSL Gateway host IP')
    parser.add_argument('--ssl_port', type=int, default=8443, help='SSL Gateway port')
    parser.add_argument('--backend_host', type=str, default='localhost', help='Backend server host IP')
    parser.add_argument('--backend_port', type=int, default=8081, help='Backend server port')
    parser.add_argument('--certfile', type=str, default='cert.pem', help='SSL certificate file')
    parser.add_argument('--keyfile', type=str, default='key.pem', help='SSL key file')

    args = parser.parse_args()

    gateway = SSLGateway(args.ssl_host, args.ssl_port, args.backend_host, args.backend_port, args.certfile, args.keyfile)
    gateway.start()

if __name__ == "__main__":
    main()

