import socket
import selectors
import types
import sys
import signal
import time

HOST = "192.168.0.103"
PORT = 3003




# Registra nova conexao
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Aceita a conexao
    print('Conexao recebida de:', addr)
    conn.setblocking(False) # Configura o socket para nao blockear o recebimento de novas conexoes
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'') # Cria atributos para o objeto data
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # Bitwise Or
    selector.register(conn, events, data=data) # registra nova conexao no selector



def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # Compara atraves da mascara se um evento de leitura ou escrita pode ser executado
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # realiza a leitura dos dados
        if recv_data:
            data.outb += recv_data
        else:
            print('Fechando conexao para:', data.addr)
            selector.unregister(sock) # retira a conexao do registro
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('Dados recebidos: ', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

selector = selectors.DefaultSelector() # registra um socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket 
lsock.bind((HOST, PORT))
lsock.listen()
lsock.setblocking(False)

print('Escutando em:', (HOST, PORT))


selector.register(lsock, selectors.EVENT_READ, data=None)


def handler(signum, frame):
    global exitFlag
    exitFlag = True
    print("Encerrando servidor...")
    lsock.close()
    SystemExit(0)


signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler) # ctrl+c


# Executa laco para aguardar conexao do cliente
while True:
    events = selector.select(timeout=None)

    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)


# DRE:Prova:Nota:Trabalho:Nota