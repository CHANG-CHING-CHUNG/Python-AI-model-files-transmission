"""
Server receiver of the file
"""
import socket
from ai_files_transmission import AiFIlesTransmission



SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT }')

def receive__AI_files_wrapper():
  while True:
    client_socket, address = s.accept() 
    print(f"[+] {address} is connected.")

    target_dir_path = "/home/john/桌面/工作/測試/AI_model_transmission/dist"
    ai_files_transmission = AiFIlesTransmission()
    result = ai_files_transmission.receive_AI_files(target_dir_path,client_socket)
    print(result)

    client_socket.close()

    print(f"[+] {address} has benn disconnected.")

receive__AI_files_wrapper()