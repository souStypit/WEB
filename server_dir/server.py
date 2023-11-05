from datetime import datetime
import socket
import time

SERVER_HOST = ''
SERVER_PORT = 9734
LOG_FILE_NAME = 'server_log.txt'
RUNTIME = 1

def timer(sec = RUNTIME):
    wait = time.perf_counter() + sec
    while time.perf_counter() < wait:
        pass

def get_time():
    return datetime.now().strftime('%a %b %Y, %H:%M:%S')

def log_connection(log_file, addr):
    time = get_time()
    log_file.write(f'{time}: {addr} connected\n')

def log_disconnection(log_file, addr):
    time = get_time()
    log_file.write(f'{time}: {addr} disconnected\n')

def log_send(log_file, send_msg):
    time = get_time()
    log_file.write(f'{time}: {send_msg}\n')

def log_recv(log_file, recv_msg):
    time = get_time()
    log_file.write(f'{time}: Client 1: {recv_msg}\n')

def main():
    log_file = open(LOG_FILE_NAME, 'w')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen()

    client_sock, client_addr = server_sock.accept()
    log_connection(log_file, client_addr)

    while True:
        dataFromClient = client_sock.recv(1024).decode()
        if not dataFromClient:
            break
        timer()
        log_recv(log_file, dataFromClient)

        dataMirrored = dataFromClient[::-1]
        data = f'{dataMirrored} {dataFromClient}'

        timer()
        client_sock.send(data.encode())
        log_send(log_file, data)

    client_sock.close()
    log_disconnection(log_file, client_addr)

    server_sock.close()
    log_file.close()

if __name__ == '__main__':
    main()