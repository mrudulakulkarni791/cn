# file_server.py
import socket
import os

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 12345
FILENAME = 'file.txt'    # file to send
CHUNK_SIZE = 65536       # 64KB

if not os.path.isfile(FILENAME):
    print(f"File '{FILENAME}' not found. Put the file in the same folder.")
    raise SystemExit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"File server listening on {HOST}:{PORT} ...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        # Optionally receive a request message (e.g. "GET")
        request = conn.recv(1024).decode('utf-8')
        print("Client request:", request)

        # Send file in binary chunks
        with open(FILENAME, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                conn.sendall(chunk)
        # Optionally send end marker or a small message
        # conn.sendall(b'__END__')   # not required if client just closes on EOF
        print("Done sending file.")
