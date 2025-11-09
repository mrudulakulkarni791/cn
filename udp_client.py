import socket
import os

# 1️⃣ Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2️⃣ Server details
server_address = ('127.0.0.1', 8885)

# 3️⃣ Get filename
filename = input("Enter filename to send (with extension): ")

if not os.path.exists(filename):
    print("⚠️ File not found!")
    client_socket.close()
    exit()

# 4️⃣ Send file name
client_socket.sendto(filename.encode(), server_address)

# 5️⃣ Read and send file in chunks
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(1024)
        if not bytes_read:
            break
        client_socket.sendto(bytes_read, server_address)

# 6️⃣ Send end signal
client_socket.sendto("EOF".encode(), server_address)
print("✅ File sent successfully!")

client_socket.close()
