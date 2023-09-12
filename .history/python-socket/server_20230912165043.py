'''
Arthur Valls da Costa Silva (120177470)
Julia Turazzi Almeida (120188861)
'''

from socket import *
import sys

HOST = "127.0.0.1"  # localhost
PORT = 12345  # porta 

# usuário cadastrado
USER = "arthur"
PASSWORD = "1234"

# flag pra fazer track da autenticação do usuário
authenticated = False

# função para carregar as páginas HTML
def serve_page(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "404 Not Found"


serverSocket = socket(AF_INET, SOCK_STREAM) # cria um socket usando IPv4 e o protocolo TCP
serverSocket.bind((HOST, PORT)) # associa o socket criado ao endereço e porta especificados
serverSocket.listen(1) # coloca o socket em modo escuta, permitindo apenas uma conexão

# printa no terminal o URL pra acessar a página HTML
print(f"Acesse o seguinte URL no navegador: http://{HOST}:{PORT}")

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    print("Conectado com:", addr)
    try:
        message = connectionSocket.recv(2048).decode()  # recebe a mensagem e a decodifica

        if "GET /" in message:
            # página inicial com o formulário de login
            response = f"""HTTP/1.1 200 OK

{serve_page('index.html')}
"""
        elif "POST /login" in message:
            lines = message.split("\r\n") # divide a mensagem recebida em linhas
            login_attempt = lines[-1] # ultima linha contem a tentiva de login no seguinte formato "user=usuario&password=senha"
            
            # realiza a autenticação do usuário
            if login_attempt == f"user={USER}&password={PASSWORD}":
                authenticated = True
            
            # redireciona para a página de sucesso ou erro
            if authenticated:
                response = f"""HTTP/1.1 200 OK

{serve_page('success.html')}
"""
            else:
                response = f"""HTTP/1.1 200 OK

{serve_page('error.html')}
"""
        elif "POST /logout" in message:
            # faz o logout, setando a autenticação para não autenticado
            authenticated = False
            # redireciona de volta para a página de login
            response = """HTTP/1.1 302 Found
Location: /
"""
        # envia a resposta para o navegador
        connectionSocket.sendall(response.encode())
        connectionSocket.close()
    except IOError:
        pass
serverSocket.close()
sys.exit()
