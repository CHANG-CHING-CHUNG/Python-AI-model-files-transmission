"""
Client that sends the file (uploads)
"""
import socket
from ai_files_transmission import AiFIlesTransmission
import threading


DIRECTORY_PATH = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-06-23_z/1"
DIRECTORY_PATH2 = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-07-03_z/2"
DIRECTORY_PATH3 = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-07-04_z/3"
DIRECTORY_PATH4 = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-07-05_z/4"
DIRECTORY_PATH5 = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-07-06_z/5"



def send_AI_files_wrapper(host, port, path):

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    ai_files_transmission = AiFIlesTransmission()
    result = ai_files_transmission.start_sending_AI_files(path,s)
    print(result)

    s.close()

send_AI_files_wrapper("0.0.0.0",5001,DIRECTORY_PATH)
# t1 = threading.Thread(target=send_AI_files_wrapper, args=("0.0.0.0",5001, DIRECTORY_PATH)).start()
# t2 = threading.Thread(target=send_AI_files_wrapper, args=("0.0.0.0",5001, DIRECTORY_PATH2)).start()
# t3 = threading.Thread(target=send_AI_files_wrapper, args=("0.0.0.0",5001, DIRECTORY_PATH3)).start()


