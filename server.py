"""
Server receiver of the file
"""
import socket
import os
import json

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

# receive 4096 bytes each time
BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT }')


def save_h5_file(client_socket):
  CHUNK_SIZE = 8 * 1024
  chunk = client_socket.recv(CHUNK_SIZE)
  file = open('test1.h5','wb')
  while chunk:
    chunk = client_socket.recv(CHUNK_SIZE) 
    file.write(chunk)

def save_json_file(client_socket):
  CHUNK_SIZE = 8 * 1024
  chunk = client_socket.recv(CHUNK_SIZE).decode('utf-8')
  chunk = json.loads(chunk)
  with open("test1.json", "w") as file:
    json.dump(chunk, file)

def receive_file():
  while True:
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    save_h5_file(client_socket)
    # close the client socket
    client_socket.close()
    # close the server socket
    print(f"[+] {address} has benn disconnected.")

receive_file()