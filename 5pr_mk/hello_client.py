# hello_client.py
import socket

HOST = '127.0.0.1'   # server IP or 'localhost'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "Hello"
    s.sendall(message.encode('utf-8'))   # send bytes
    data = s.recv(1024)                  # receive reply
    if data:
        print("Server Says:", data.decode('utf-8'))
    else:
        print("No reply from server.")
