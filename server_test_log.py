"""
Server receiver of the file
"""
import socket
from ai_files_transmission import AiFIlesTransmission
import logging
import time
import datetime


current_date = datetime.datetime.now()
current_date = current_date.strftime("%Y-%m-%d")
logging.basicConfig(filename=f"{current_date}-after-ai_file-download.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

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

    start_time = time.time()
    logging.info('優化後 AI 模型檔案下載速度測試開始')

    result = ai_files_transmission.receive_AI_files(target_dir_path,client_socket)


    end_time = time.time()  
    elapsed_time = end_time - start_time
    logging.info('優化後 AI 模型檔案下載速度測試結束')
    logging.info(f'下載花費時間: {elapsed_time}')
    logging.info('\n')

    print("result",result)

    client_socket.close()

    print(f"[+] {address} has benn disconnected.")



receive__AI_files_wrapper()