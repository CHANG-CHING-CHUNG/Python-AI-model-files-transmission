"""
Client that sends the file (uploads)
"""
import socket
from os import walk, path
import re
import json
import h5py
import numpy as np
import select
import os
SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 8 * 1024

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
    total_bytes = socket.sendfile(file)
    print(total_bytes)

def open_and_send_log_file(file_to_be_sent,socket):
    BUFFER_SIZE = 8 * 1024
    with open(file_to_be_sent,'rb') as file:
        while True:
          bytes_read = file.read(BUFFER_SIZE)
          if not bytes_read:
            break
          total_bytes = socket.sendall(bytes_read)

def open_and_send_csv_file(file_to_be_sent,socket):
    BUFFER_SIZE = 8 * 1024
    with open(file_to_be_sent,'rb') as file:
        while True:
          bytes_read = file.read(BUFFER_SIZE)
          if not bytes_read:
            break
          socket.sendall(bytes_read)

def open_and_sned_json_file(file_to_be_sent,socket):
    file = open(file_to_be_sent)
    json_data = json.load(file)
    json_str = json.dumps(json_data)
    socket.sendall(bytes(json_str,encoding='utf-8'))

def send_AI_file_list(DIRECTORY_PATH,socket):
    AI_file_list = get_all_AI_filenames(DIRECTORY_PATH)
    AI_file_list_json_str = json.dumps(AI_file_list)
    socket.sendall(AI_file_list_json_str.encode("utf-8"))

def send_file(host, port):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    AI_file_list = get_all_AI_filenames(DIRECTORY_PATH)
    for AI_file in AI_file_list:

      AI_file_path = path.join(AI_file["path"],AI_file["filename"])
      # print(AI_file_path)
      if len(re.findall(".h5$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_h5_file(AI_file_path,s)
        s.settimeout(10)
        try:
          response = s.recv(1024).decode("utf-8")
          print(response)
        except:
          print("why")
          continue
      elif len(re.findall(".log$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_log_file(AI_file_path,s)
        s.settimeout(10)
        try:
          response = s.recv(1024).decode("utf-8")
          print(response)
        except:
          print("why")
          continue
      elif len(re.findall(".h5last$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_h5_file(AI_file_path,s)
        s.settimeout(10)
        try:
          response = s.recv(1024).decode("utf-8")
          print(response)
        except:
          print("why")
          continue
      elif len(re.findall(".csv$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_send_csv_file(AI_file_path,s)
        s.settimeout(10)
        try:
          response = s.recv(1024).decode("utf-8")
          print(response)
        except:
          print("why")
          continue
      elif len(re.findall(".json$",AI_file["filename"])):
        print("found it! ",AI_file["filename"])
        open_and_sned_json_file(AI_file_path,s)
        s.settimeout(10)
        try:
          response = s.recv(1024).decode("utf-8")
          print(response)
        except:
          print("why")
          continue
      
      

    s.close()

send_file("0.0.0.0",5001)

