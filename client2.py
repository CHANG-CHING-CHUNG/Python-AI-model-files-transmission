"""
Client that sends the file (uploads)
"""
import socket
from ai_files_transmission import AiFIlesTransmission


DIRECTORY_PATH2 = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-07-03_z/2"


def send_AI_files_wrapper(host, port):

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    ai_files_transmission = AiFIlesTransmission()
    result = ai_files_transmission.start_sending_AI_files(DIRECTORY_PATH2,s)
    print(result)

    s.close()

send_AI_files_wrapper("0.0.0.0",5001)

