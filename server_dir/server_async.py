from datetime import datetime
import socket
import asyncio

SERVER_HOST = ''
SERVER_PORT = 9734
LOG_FILE_NAME = './server_dir/server_log.log'
RUNTIME = 10

async def timer(sec=RUNTIME):
    await asyncio.sleep(sec)

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

def log_recv(log_file, recv_msg, addr):
    time = get_time()
    log_file.write(f'{time}: Client {addr}: {recv_msg}\n')

async def handle_client(client_sock, client_addr, log_file):
    log_connection(log_file, client_addr)

    while True:
        dataFromClient = await loop.sock_recv(client_sock, 1024)
        dataFromClient = dataFromClient.decode()
        if not dataFromClient:
            break
        await timer()
        log_recv(log_file, dataFromClient, client_addr)

        dataMirrored = dataFromClient[::-1]
        data = f'{dataMirrored} Сервер написал Савенков И.В. М3О-419Бк-20'

        await timer()
        await loop.sock_sendall(client_sock, data.encode())
        log_send(log_file, data)
    
    client_sock.close()
    log_disconnection(log_file, client_addr)

async def main():
    log_file = open(LOG_FILE_NAME, 'a')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_HOST, SERVER_PORT))
    server_sock.listen()
    server_sock.setblocking(False)

    while True:
        client_sock, client_addr = await loop.sock_accept(server_sock)
        loop.create_task(handle_client(client_sock, client_addr, log_file))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close