#!/usr/bin/env python3
# server.py
# Simple TCP server that supports: HELLO, CALC <expr>, GET <filename>, PUT <filename>.

import socket
import os
import ast
import operator

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 5001

# Safe eval for arithmetic expressions using ast
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def safe_eval(expr):
    """
    Evaluate a math expression safely (numbers, + - * / % // **, parentheses).
    Raises ValueError on invalid input.
    """
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):  # <number>
            return node.n
        if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.UAdd, ast.USub):
            return ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[type(node.op)](left, right)
        raise ValueError("Unsupported expression")
    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed)

def recv_line(conn):
    """Receive a line terminated by '\n' (UTF-8)"""
    data = b''
    while True:
        ch = conn.recv(1)
        if not ch:
            return None
        data += ch
        if ch == b'\n':
            break
    return data.decode('utf-8').rstrip('\n')

def recv_all(conn, n):
    """Receive exactly n bytes (or None if connection closed)"""
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    try:
        while True:
            line = recv_line(conn)
            if line is None:
                print("Client disconnected")
                break
            if not line:
                continue
            parts = line.split(' ', 1)
            cmd = parts[0].upper()
            arg = parts[1] if len(parts) > 1 else ''

            if cmd == 'HELLO':
                conn.sendall(b"Hello, client!\n")

            elif cmd == 'CALC':
                expr = arg.strip()
                try:
                    result = safe_eval(expr)
                    conn.sendall(f"RESULT {result}\n".encode())
                except Exception as e:
                    conn.sendall(f"ERROR invalid expression: {e}\n".encode())

            elif cmd == 'GET':
                filename = arg.strip()
                if not filename or not os.path.exists(filename):
                    conn.sendall(b"ERROR file not found\n")
                else:
                    filesize = os.path.getsize(filename)
                    conn.sendall(f"OK {filesize}\n".encode())
                    with open(filename, 'rb') as f:
                        # send file bytes
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            conn.sendall(chunk)

            elif cmd == 'PUT':
                # client will send "PUT filename filesize"
                try:
                    fname_filesize = arg.strip().split()
                    if len(fname_filesize) != 2:
                        conn.sendall(b"ERROR usage: PUT filename filesize\n")
                        continue
                    filename = fname_filesize[0]
                    filesize = int(fname_filesize[1])
                except:
                    conn.sendall(b"ERROR invalid parameters\n")
                    continue

                conn.sendall(b"OK\n")  # ready to receive
                data = recv_all(conn, filesize)
                if data is None:
                    print("Client closed during upload")
                    break
                # save uploaded file
                with open("uploaded_" + os.path.basename(filename), 'wb') as f:
                    f.write(data)
                conn.sendall(b"UPLOAD_DONE\n")

            elif cmd == 'QUIT':
                conn.sendall(b"BYE\n")
                break

            else:
                conn.sendall(b"ERROR unknown command\n")
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Connection closed.")

def main():
    print("Starting simple TCP server on port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)  # single client at a time (simple)
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == '__main__':
    main()
