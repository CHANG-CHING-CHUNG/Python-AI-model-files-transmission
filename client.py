"""
Client that sends the file (uploads)
"""
import socket
from os import walk, path
import re
import json
import struct

DIRECTORY_PATH = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-06-23_z/1"

def get_all_AI_filenames(directory_path):
  AI_file_list = []
  
  for (dirpath, dirnames, filenames) in walk(directory_path):
    
    for file in filenames:
      if len(re.findall(".h5$|.log$|.h5last$|.csv$|.json$", file)):
        ai_file ={
          "path":dirpath,
          "filename":file
        }

        AI_file_list.append(ai_file)

  return AI_file_list

def open_and_send_h5_file(file_to_be_sent,socket):
  with open(file_to_be_sent, 'rb') as file:
    file_data = file.read()
    length = struct.pack('>Q', len(file_data))
    print(int.from_bytes(length,"big"))
    socket.sendall(length)
    socket.sendall(file_data)
    response = socket.recv(1)
    return response

def open_and_send_log_file(file_to_be_sent,socket):
    with open(file_to_be_sent,'rb') as file:
      file_data = file.read()
      length = struct.pack('>Q', len(file_data))
      socket.sendall(length)
      socket.sendall(file_data)
      response = socket.recv(1)
      return response


def open_and_send_csv_file(file_to_be_sent,socket):
    with open(file_to_be_sent,'rb') as file:
      file_data = file.read()
      length = struct.pack('>Q', len(file_data))
      socket.sendall(length)
      socket.sendall(file_data)
      response = socket.recv(1)
      return response


def open_and_send_json_file(file_to_be_sent,socket):
    with open(file_to_be_sent, 'rb') as file:
      file_data = file.read()
      length = struct.pack('>Q', len(file_data))
      socket.sendall(length)
      socket.sendall(file_data)
      response = socket.recv(1)
      return response


def send_AI_file_list(DIRECTORY_PATH,socket):
    AI_file_list = get_all_AI_filenames(DIRECTORY_PATH)
    AI_file_list_json_str = json.dumps(AI_file_list)
    length = struct.pack('>Q',len(AI_file_list_json_str.encode("utf-8")))
    socket.sendall(length)
    socket.sendall(AI_file_list_json_str.encode("utf-8"))
    response = socket.recv(1)
    return response


def send_AI_files(DIRECTORY_PATH,socket):
    AI_file_list = get_all_AI_filenames(DIRECTORY_PATH)
    for AI_file in AI_file_list:
      AI_file_path = path.join(AI_file["path"],AI_file["filename"])
      print(AI_file_path)
      if len(re.findall(".h5$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        response = open_and_send_log_file(AI_file_path,socket)
      elif len(re.findall(".log$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_h5_file(AI_file_path,socket)
      elif len(re.findall(".h5last$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_h5_file(AI_file_path,socket)
      elif len(re.findall(".csv$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_csv_file(AI_file_path,socket)
      elif len(re.findall(".json$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_json_file(AI_file_path,socket)
      if response != b'\x00':
        return False

def send_file(host, port):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    response = send_AI_file_list(DIRECTORY_PATH,s)
    if response:
      send_AI_files(DIRECTORY_PATH,s)

      
      

    s.close()

send_file("0.0.0.0",5001)

