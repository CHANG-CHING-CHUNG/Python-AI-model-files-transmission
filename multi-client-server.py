import socket
import select
import threading
from ai_files_transmission import AiFIlesTransmission

def run_receive_model():
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 5001

    server = socket.socket()

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.setblocking(0)  # socket設成「非阻塞」模式
    server.listen(5)
    print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT }')
    inputs = [server]
    clients = []

    while True:
        path = "/home/john/桌面/工作/測試/AI_model_transmission/dist"
        for client in clients:
            print(client.fileno())
        readable, _, _ = select.select(inputs, [], [])
        for sck in readable:
            if sck is server:
                client, addr = sck.accept()
                clients.append(client)
                t1 = threading.Thread(target=AiFIlesTransmission().receive_AI_files, args=(path,client)).start()
                t1.join()

run_receive_model()