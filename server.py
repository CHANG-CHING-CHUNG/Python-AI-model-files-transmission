"""
Server receiver of the file
"""
import socket
import os
import json
import h5py
import select

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


def save_h5_and_h5last_file(client_socket,file_format):
  CHUNK_SIZE = 8 * 1024
  if file_format == '.h5':
    file = open('test2.h5','wb')
  elif file_format == '.h5last':
    file = open('test2.h5last','wb')
  client_socket.settimeout(1)
  while True:
    try:
      chunk = client_socket.recv(CHUNK_SIZE)
    except:
      break
    file.write(chunk)
  file.close()

def save_log_file(client_socket):
    CHUNK_SIZE = 8 * 1024
    file = open('test3.log','wb')
    client_socket.settimeout(1)
    while True:
      try:
        chunk = client_socket.recv(CHUNK_SIZE)
      except:
        break
      file.write(chunk)
    file.close()

def save_csv_file(client_socket):
    CHUNK_SIZE = 8 * 1024
    file = open('test4.csv','wb')
    client_socket.settimeout(1)
    while True:
      try:
        chunk = client_socket.recv(CHUNK_SIZE)
      except:
        break
      file.write(chunk)
  
    file.close()

def save_json_file(client_socket):
    CHUNK_SIZE = 8 * 1024
    data = ""
    client_socket.settimeout(1)
    while True:
      try:
        chunk = client_socket.recv(CHUNK_SIZE).decode('utf-8')
      except:
        break
      data = data + chunk
    if data:
      json_data = json.loads(data)
      with open("test1.json", "w") as file:
        json.dump(json_data, file)

def receive_AI_file_json_list(client_socket):
    CHUNK_SIZE = 8 * 1024
    data = ""
    client_socket.settimeout(1)
    while True:
      try:
        chunk = client_socket.recv(CHUNK_SIZE).decode("utf-8")
      except:
        break
      data  = data + chunk
    json_data_list = json.loads(data)
    return json_data_list

def receive_file_size(client_socket):
    data = ""
    client_socket.settimeout(1)
    while True:
      try:
        chunk = client_socket.recv(1024).decode("utf-8")
        data = data + chunk
      except:
        break
    return data

def receive_file():
  while True:
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    # Ai_file_list = receive_AI_file_json_list(client_socket)
    # print(Ai_file_list)
    save_h5_and_h5last_file(client_socket,".h5")
    client_socket.sendall("ok".encode("utf-8"))
    save_log_file(client_socket)
    client_socket.sendall("ok".encode("utf-8"))
    save_h5_and_h5last_file(client_socket,".h5last")
    client_socket.sendall("ok".encode("utf-8"))
    save_csv_file(client_socket)
    client_socket.sendall("ok".encode("utf-8"))
    save_json_file(client_socket)
    client_socket.sendall("ok".encode("utf-8"))


    # client_socket.sendall("success".encode("utf-8"))
    # close the client socket
    client_socket.close()
    # close the server socket
    print(f"[+] {address} has benn disconnected.")

receive_file()