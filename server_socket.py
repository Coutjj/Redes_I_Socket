import socket
import selectors
import types


HOST = "192.168.0.103"
PORT = 3003


# Funcao para processar dados recebidos
def read_and_save_grades(grades):
    data = grades.decode("utf-8")
    data = data.split(":")
    if len(data) < 3 or len(data) > 3:
        print("Uso incorreto do protocolo de dados...")

    print("DRE: ", data[0])
    print("Tipo de avaliacao: ", data[1])
    print("Nota: ", data[2])

    save(data[0], data[1], data[2])


# salva dados em arquivo
def save(dre, tipo_avaliacao, nota):
    with open("notas.txt", "a") as text_file:
        text_file.write(dre + ":" + tipo_avaliacao + ":" + nota + "\n")



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
            print('Dados recebidos: ', str(data.outb, 'UTF-8'))
            read_and_save_grades(data.outb)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


selector = selectors.DefaultSelector() # registra um socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket 
lsock.bind((HOST, PORT))
lsock.listen()
lsock.setblocking(False)

print('Escutando em:', (HOST, PORT))


selector.register(lsock, selectors.EVENT_READ, data=None)

# https://github.com/codypiersall/pynng/issues/49 motivo pelo qual o signal handler nao funciona
# def handler(signum, frame):
#     print("Encerrando servidor...")
#     lsock.close()
#     SystemExit(0)


# signal.signal(signal.SIGTERM, handler)
# signal.signal(signal.SIGINT, handler)


# Executa laco para aguardar conexao do cliente
while True:
    events = selector.select(timeout=None)

    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
