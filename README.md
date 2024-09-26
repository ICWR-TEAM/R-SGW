# R-SGW - SSL Gateway

This repository contains a Python script for creating an SSL Gateway that securely forwards traffic between clients and a backend server. The SSL Gateway uses self-signed certificates for encryption, making it suitable for testing and development environments.

## Features

- Automatically generates a self-signed SSL certificate if none exists.
- Listens for incoming SSL connections and forwards data to a specified backend server.
- Handles SSL encryption and decryption using Python's `ssl` and `OpenSSL` libraries.

## Requirements

- Python 3.x
- `pyOpenSSL` library (can be installed via pip)

```bash
pip install pyOpenSSL
```

## Usage

You can run the SSL Gateway with command-line arguments to specify configuration options.

### Command Line Arguments

- `--ssl_host`: Host IP for the SSL Gateway (default: `localhost`)
- `--ssl_port`: Port for the SSL Gateway (default: `8443`)
- `--backend_host`: Host IP for the backend server (default: `localhost`)
- `--backend_port`: Port for the backend server (default: `8081`)
- `--certfile`: Path to the SSL certificate file (default: `cert.pem`)
- `--keyfile`: Path to the SSL key file (default: `key.pem`)

### Example Command

```bash
python your_script.py --ssl_host 0.0.0.0 --ssl_port 8443 --backend_host 192.168.1.100 --backend_port 8081
```

## How It Works

1. **Self-Signed Certificate Generation**: If the specified certificate or key files do not exist, the script generates a self-signed certificate and private key.

2. **Start SSL Gateway**: The SSL Gateway listens for incoming SSL connections on the specified host and port.

3. **Forward Data**: Once a connection is established, it forwards data between the client and the specified backend server, handling SSL encryption and decryption transparently.

## Example Output

When running the script, you should see output similar to:

```
SSL Gateway is running on localhost:8443, forwarding to localhost:8081...
SSL Connection from ('127.0.0.1', 12345)
SSL connection established with ('127.0.0.1', 12345)
Connected to backend localhost:8081
```

## License

This project is licensed under the MIT License. Feel free to modify and use it as needed.

## Contributing

If you want to contribute, please fork the repository and create a pull request with your changes. Any improvements or bug fixes are welcome!

## Author

This script was developed by **Afrizal F.A** as part of R&D at ICWR. For any inquiries, please reach out via afrzlf4@gmail.com.
