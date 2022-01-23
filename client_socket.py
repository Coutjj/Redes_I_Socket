import socket


dre = input("Digite o DRE do aluno:\t")
aval1= input("Digite nome da avaliacao:\t")
notaAval1= input("Digite a nota da prova:\t")

dataRegistro = dre + ":" + aval1 + ":" + notaAval1

HOST = "limahost.duckdns.org"# ip publico do servidor 
PORT = 1080# porta de acesso ao servidor


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(bytes(dataRegistro.encode()))
