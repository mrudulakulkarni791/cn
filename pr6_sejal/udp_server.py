# Program: UDP File Transfer Server
# Author: (Your Name)
# Subject: Computer Networks Laboratory

import socket

# Step 1: Define server IP and Port
SERVER_IP = "0.0.0.0"   # Listen on all available interfaces
SERVER_PORT = 5005
BUFFER_SIZE = 4096

# Step 2: Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Server is listening on port {SERVER_PORT}...")

while True:
    # Step 3: Receive filename first
    print("\nWaiting for file...")
    filename, client_addr = server_socket.recvfrom(BUFFER_SIZE)
    filename = filename.decode()
    print(f"Receiving file: {filename} from {client_addr}")

    # Step 4: Open new file to write incoming data
    with open("received_" + filename, "wb") as f:
        while True:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            if data == b"EOF":
                print("File transfer complete.")
                break
            f.write(data)

    print(f"File saved successfully as received_{filename}\n")
