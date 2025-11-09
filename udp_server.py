import socket

# 1️⃣ Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2️⃣ Bind to IP and port
server_address = ('127.0.0.1', 8885)
server_socket.bind(server_address)
print("🎧 Server ready and waiting for file...")

# 3️⃣ Receive file name
filename, client_addr = server_socket.recvfrom(1024)
filename = filename.decode()
print(f"Receiving file: {filename}")

# 4️⃣ Open file to write binary data
with open("received_" + filename, "wb") as f:
    while True:
        data, addr = server_socket.recvfrom(1024)
        if data.decode(errors='ignore') == "EOF":
            print("✅ File transfer completed successfully!")
            break
        f.write(data)

server_socket.close()
print(f"📁 File saved as received_{filename}")
