# file_client.py
import socket

HOST = '127.0.0.1'  # server IP
PORT = 12345
OUTFILE = 'received_file'   # where to save

CHUNK_SIZE = 65536

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Optionally inform server what you want
    s.sendall(b'Hello server! Please send file')
    print("Request sent, receiving file...")

    with open(OUTFILE, 'wb') as f:
        while True:
            data = s.recv(CHUNK_SIZE)
            if not data:
                break
            f.write(data)

    print("File received and saved as:", OUTFILE)
