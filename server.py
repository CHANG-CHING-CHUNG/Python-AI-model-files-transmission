"""
Server receiver of the file
"""
import socket
import os
import json
import struct
import pathlib
import re
import binascii



# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

# create the server socket
# TCP socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT }')


def save_h5_and_h5last_file(client_socket,file_format, save_file_path):
  CHUNK_SIZE = 8 * 1024
  if file_format == '.h5':
    file = open(save_file_path,'wb')
  elif file_format == '.h5last':
    file = open(save_file_path,'wb')
  bs = client_socket.recv(8)
  (length,) = struct.unpack('>Q',bs)
  print(length)
  data = b''
  while len(data) < length:
    to_read = int(length) - int(len(data))
    data += client_socket.recv(min(CHUNK_SIZE, to_read))
    if to_read == 0:
      break
  client_socket.sendall(b'\00')
  file.write(data)
  print(crc32(save_file_path))
  file.close()

def save_log_file(client_socket,save_file_path):
    CHUNK_SIZE = 8 * 1024
    file = open(save_file_path,'wb')
    bs = client_socket.recv(8)
    (length,) = struct.unpack('>Q',bs)
    data = b''
    print(length)
    while len(data) < length:
      to_read = int(length) - int(len(data))
      data += client_socket.recv(min(CHUNK_SIZE, to_read))
      if to_read == 0:
        break
    client_socket.sendall(b'\00')
    file.write(data)
    file.close()

def save_csv_file(client_socket,save_file_path):
    CHUNK_SIZE = 8 * 1024
    file = open(save_file_path,'wb')
    bs = client_socket.recv(8)
    (length,) = struct.unpack('>Q',bs)
    data = b''
    print(length)
    while len(data) < length:
      to_read = int(length) - int(len(data))
      data += client_socket.recv(min(CHUNK_SIZE, to_read))
      if to_read == 0:
        break
    client_socket.sendall(b'\00')
    file.write(data)
    file.close()

def save_json_file(client_socket,save_file_path):
    CHUNK_SIZE = 8 * 1024
    file = open(save_file_path,'wb')
    bs = client_socket.recv(8)
    (length,) = struct.unpack('>Q',bs)
    data = b''
    print(length)
    while len(data) < length:
      to_read = int(length) - int(len(data))
      data += client_socket.recv(min(CHUNK_SIZE, to_read))
      if to_read == 0:
        break
    client_socket.sendall(b'\00')
    file.write(data)



def receive_AI_files(client_socket,save_file_path):
    save_h5_and_h5last_file(client_socket,".h5",save_file_path)
    save_log_file(client_socket,save_file_path)
    save_h5_and_h5last_file(client_socket,".h5last",save_file_path)
    save_csv_file(client_socket,save_file_path)
    save_json_file(client_socket,save_file_path)

def receive_AI_file_json_list(client_socket):
    bs = client_socket.recv(8)
    (length,) = struct.unpack('>Q',bs)
    data = b''
    print(length)
    while len(data) < length:
      to_read = int(length) - int(len(data))
      data += client_socket.recv(min(8 * 1024, to_read))
      if to_read == 0:
        break
    AI_file_json_list = json.loads(data.decode("utf-8"))
    client_socket.sendall(b'\00')
    return AI_file_json_list


def crc32(filename):
    buf = open(filename,'rb').read()
    hash = binascii.crc32(buf) & 0xFFFFFFFF
    return "%08X" % hash


def receive_file():
  while True:
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    target_dir_path = "/home/john/桌面/工作/測試/AI_model_transmission/dist"
    AI_file_json_list = receive_AI_file_json_list(client_socket)
    print(AI_file_json_list)
    for AI_file in AI_file_json_list:
      sub_dir = AI_file['path'].split("/")[-1]
      target_dir_full_path = os.path.join(target_dir_path,sub_dir)
      path = pathlib.Path(target_dir_full_path)
      path.mkdir(parents=True, exist_ok=True)
      save_file_path = os.path.join(target_dir_full_path, AI_file["filename"])
      if len(re.findall(".h5$",AI_file["filename"])):
        save_h5_and_h5last_file(client_socket,".h5",save_file_path)
      elif len(re.findall(".log$",AI_file["filename"])):
        save_log_file(client_socket,save_file_path)
      elif len(re.findall(".h5last$",AI_file["filename"])):
        save_h5_and_h5last_file(client_socket,".h5last",save_file_path)
      elif len(re.findall(".csv$",AI_file["filename"])):
        save_csv_file(client_socket,save_file_path)
      elif len(re.findall(".json$",AI_file["filename"])):
        save_json_file(client_socket,save_file_path)

    # client_socket.sendall("success".encode("utf-8"))
    # close the client socket
    client_socket.close()
    # close the server socket
    print(f"[+] {address} has benn disconnected.")

receive_file()