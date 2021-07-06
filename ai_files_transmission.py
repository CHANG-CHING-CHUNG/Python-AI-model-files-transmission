from os import walk
import os
import re
import json
import struct
import binascii
import pathlib

class AiFIlesTransmission:
  
  def get_all_AI_filenames(self, directory_path):
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

  def open_and_send_AI_files(self, file_to_be_sent,socket):
    with open(file_to_be_sent, 'rb') as file:
      file_data = file.read()
      length = struct.pack('>Q', len(file_data))
      socket.sendall(length)
      socket.sendall(file_data)
      response = socket.recv(1)
      return response


  def send_AI_file_list(self, DIRECTORY_PATH,socket):
      AI_file_list = self.get_all_AI_filenames(DIRECTORY_PATH)
      AI_file_list_with_crc = self.cal_file_crc(AI_file_list)
      AI_file_list_json_str = json.dumps(AI_file_list_with_crc)
      length = struct.pack('>Q',len(AI_file_list_json_str.encode("utf-8")))
      socket.sendall(length)
      socket.sendall(AI_file_list_json_str.encode("utf-8"))
      response = socket.recv(1)
      return response

  def cal_file_crc(self, AI_file_list):
      for AI_file in AI_file_list:
        file_full_path = os.path.join(AI_file["path"], AI_file["filename"])
        checksum = self.crc32(file_full_path)
        AI_file["checksum"] = checksum
      return AI_file_list

  def send_AI_files(self, DIRECTORY_PATH,socket):
      response = None
      AI_file_list = self.get_all_AI_filenames(DIRECTORY_PATH)
      for AI_file in AI_file_list:
        AI_file_path = os.path.join(AI_file["path"],AI_file["filename"])
        if len(re.findall(".h5$",AI_file["filename"])):
          response = self.open_and_send_AI_files(AI_file_path,socket)
        elif len(re.findall(".log$",AI_file["filename"])):
          response = self.open_and_send_AI_files(AI_file_path,socket)
        elif len(re.findall(".h5last$",AI_file["filename"])):
          response = self.open_and_send_AI_files(AI_file_path,socket)
        elif len(re.findall(".csv$",AI_file["filename"])):
          response = self.open_and_send_AI_files(AI_file_path,socket)
        elif len(re.findall(".json$",AI_file["filename"])):
          response = self.open_and_send_AI_files(AI_file_path,socket)

        if response == b'\x01':
          return False

      return True

  def crc32(self, filename):
      buf = open(filename,'rb').read()
      hash = binascii.crc32(buf) & 0xFFFFFFFF
      return "%08X" % hash

  def start_sending_AI_files(self, DIRECTORY_PATH, socket):
      response = self.send_AI_file_list(DIRECTORY_PATH,socket)
      if response == b'\x01':
        print("something went wrong")
        return False
      result = self.send_AI_files(DIRECTORY_PATH,socket)

      if not result:
        print("something went wrong")
        return False

      print("All Ai_files are sent")
      return True

  def save_AI_files(self, client_socket, save_file_path, checksum):
    CHUNK_SIZE = 8 * 1024
    file = open(save_file_path,'wb')
    bs = client_socket.recv(8)
    (length,) = struct.unpack('>Q',bs)
    data = b''
    while len(data) < length:
      to_read = int(length) - int(len(data))
      if to_read == 0:
        break
      data += client_socket.recv(min(CHUNK_SIZE, to_read))
    file.write(data)
    file.close()
    saved_file_checksum = self.crc32(save_file_path)
    if saved_file_checksum != checksum:
      client_socket.sendall(b'\x01')
      return False
    client_socket.sendall(b'\x00')
    return True

  def receive_AI_file_json_list(self, client_socket):
      bs = client_socket.recv(8)
      (length,) = struct.unpack('>Q',bs)
      data = b''
      while len(data) < length:
        to_read = int(length) - int(len(data))
        if to_read == 0:
          break
        data += client_socket.recv(min(8 * 1024, to_read))
      AI_file_json_list = json.loads(data.decode("utf-8"))
      client_socket.sendall(b'\x00')
      return AI_file_json_list


  def receive_AI_files(self, target_dir_path,client_socket):
      AI_file_json_list = self.receive_AI_file_json_list(client_socket)
      result = None
      for AI_file in AI_file_json_list:
        sub_dir = AI_file['path'].split("/")[-1]
        target_dir_full_path = os.path.join(target_dir_path,sub_dir)
        path = pathlib.Path(target_dir_full_path)
        path.mkdir(parents=True, exist_ok=True)
        save_file_path = os.path.join(target_dir_full_path, AI_file["filename"])
        if len(re.findall(".h5$",AI_file["filename"])):
          result = self.save_AI_files(client_socket,save_file_path, AI_file["checksum"])
        elif len(re.findall(".log$",AI_file["filename"])):
          result = self.save_AI_files(client_socket,save_file_path,AI_file["checksum"])
        elif len(re.findall(".h5last$",AI_file["filename"])):
          result = self.save_AI_files(client_socket,save_file_path,AI_file["checksum"])
        elif len(re.findall(".csv$",AI_file["filename"])):
          result = self.save_AI_files(client_socket,save_file_path,AI_file["checksum"])
        elif len(re.findall(".json$",AI_file["filename"])):
          result = self.save_AI_files(client_socket,save_file_path,AI_file["checksum"])
        
        if not result:
          return result

      client_socket.close()

      return result
