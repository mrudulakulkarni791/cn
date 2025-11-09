#!/usr/bin/env python3
# client.py
# Simple interactive client to use HELLO, CALC, GET, PUT with the server.

import socket
import sys
import os

def recv_line(sock):
    data = b''
    while True:
        ch = sock.recv(1)
        if not ch:
            return None
        data += ch
        if ch == b'\n':
            break
    return data.decode('utf-8').rstrip('\n')

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

if len(sys.argv) < 2:
    print("Usage: python3 client.py SERVER_IP [PORT]")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    print("Commands: HELLO | CALC <expression> | GET <filename> | PUT <filename> | QUIT")
    while True:
        cmd = input("Enter command: ").strip()
        if not cmd:
            continue
        parts = cmd.split(' ', 1)
        verb = parts[0].upper()

        if verb == 'PUT':
            if len(parts) != 2:
                print("Usage: PUT <local_filename>")
                continue
            local = parts[1].strip()
            if not os.path.exists(local):
                print("Local file does not exist.")
                continue
            filesize = os.path.getsize(local)
            # send PUT filename filesize
            s.sendall(f"PUT {os.path.basename(local)} {filesize}\n".encode())
            resp = recv_line(s)
            if resp is None:
                print("Server closed")
                break
            if not resp.startswith("OK"):
                print("Server error:", resp)
                continue
            # send file bytes
            with open(local, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    s.sendall(chunk)
            # wait for completion acknowledgement
            resp = recv_line(s)
            print("Server:", resp)

        elif verb == 'GET':
            if len(parts) != 2:
                print("Usage: GET <filename_on_server>")
                continue
            filename = parts[1].strip()
            s.sendall(f"GET {filename}\n".encode())
            resp = recv_line(s)
            if resp is None:
                print("Server closed")
                break
            if resp.startswith("OK "):
                size = int(resp.split()[1])
                data = recv_all(s, size)
                if data is None:
                    print("Connection lost while receiving file")
                    break
                localname = "downloaded_" + os.path.basename(filename)
                with open(localname, 'wb') as f:
                    f.write(data)
                print(f"File saved as {localname} ({len(data)} bytes)")
            else:
                print("Server:", resp)

        elif verb == 'CALC':
            if len(parts) != 2:
                print("Usage: CALC <expression>")
                continue
            expr = parts[1].strip()
            s.sendall(f"CALC {expr}\n".encode())
            resp = recv_line(s)
            print("Server:", resp)

        elif verb == 'HELLO':
            s.sendall(b"HELLO\n")
            resp = recv_line(s)
            print("Server:", resp)

        elif verb == 'QUIT':
            s.sendall(b"QUIT\n")
            resp = recv_line(s)
            print("Server:", resp)
            break

        else:
            print("Unknown command locally. Use HELLO, CALC, GET, PUT, QUIT.")
