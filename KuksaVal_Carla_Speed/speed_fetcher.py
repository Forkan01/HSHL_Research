import socket

# Configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 55555        # The port used by the server

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            if not data:
                break
            speed = data.decode()
            print(f'Vehicle Speed: {speed} km/h')

if __name__ == "__main__":
    main()
