# Program: UDP File Transfer Client
# Author: (Your Name)
# Subject: Computer Networks Laboratory

import socket
import os

SERVER_IP = "127.0.0.1"  # Change this to receiver's IP if using two machines
SERVER_PORT = 5005
BUFFER_SIZE = 4096

# Step 1: Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Step 2: Ask user for file name
filename = input("Enter the filename to send: ")

if not os.path.exists(filename):
    print("File not found!")
    client_socket.close()
    exit()

# Step 3: Send filename first
client_socket.sendto(filename.encode(), (SERVER_IP, SERVER_PORT))

# Step 4: Send file contents
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        client_socket.sendto(bytes_read, (SERVER_IP, SERVER_PORT))

# Step 5: Send end-of-file signal
client_socket.sendto(b"EOF", (SERVER_IP, SERVER_PORT))
print("File sent successfully!")

client_socket.close()
