"""
Client that sends the file (uploads)
"""
import socket
from os import walk
import re
import json
SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 1024 * 4

DIRECTORY_PATH = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-06-23_z/1"

def get_all_AI_filenames(directory_path):
  AI_file_list = []
  
  for (dirpath, dirnames, filenames) in walk(directory_path):
    
    for file in filenames:
      if len(re.findall(".h5|.log|.h5last|.csv|.json", file)):
        ai_file ={
          "path":dirpath,
          "filename":file
        }

        AI_file_list.append(ai_file)

  return AI_file_list

def open_and_send_file(file_to_be_sent,socket):
  with open(file_to_be_sent, 'rb') as file:
    total_bytes = socket.sendfile(file)
    print(total_bytes)

def send_file(host, port):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    AI_file_list = get_all_AI_filenames(DIRECTORY_PATH)
    file_to_be_sent = AI_file_list[4]['path'] + "/" + AI_file_list[4]['filename']

    file = open(file_to_be_sent)
    json_data = json.load(file)
    json_str = json.dumps(json_data)
    print(json_str)
    total_bytes = s.sendall(bytes(json_str,encoding='utf-8'))
    print(total_bytes)
    # with open(file_to_be_sent, 'rb') as file:
    #   total_bytes = s.sendfile(file)
    #   print(total_bytes)
    s.close()

send_file("0.0.0.0",5001)

