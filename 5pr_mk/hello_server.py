# hello_server.py
import socket

HOST = '0.0.0.0'   # listen on all interfaces (use '127.0.0.1' for local only)
PORT = 8000        # port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on {HOST}:{PORT} ...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        data = conn.recv(1024)            # receive bytes from client
        if not data:
            print("No data received.")
        else:
            msg = data.decode('utf-8')    # decode bytes to string
            print("Client says:", msg)
            reply = "Hi"                  # reply message
            conn.sendall(reply.encode('utf-8'))
        print("Connection closed.")
