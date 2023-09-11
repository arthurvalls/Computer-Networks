from socket import *
import sys

HOST = "127.0.0.1"  # localhost
PORT = 13029  # porta aleatória

# Usuário cadastrado
USER = "arthur"
PASSWORD = "1234"

# Variável para rastrear o estado de autenticação do usuário
authenticated = False

# Função para carregar as páginas HTML
def serve_page(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "404 Not Found"

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

# Exibe o URL que deve ser acessado no navegador
print(f"Acesse o seguinte URL no navegador: http://{HOST}:{PORT}")

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    print("Conectado com:", addr)
    try:
        message = connectionSocket.recv(2048).decode()  # Recebe a mensagem e a decodifica

        if "GET /" in message:
            # Página inicial, exibe o formulário de login
            response = f"""HTTP/1.1 200 OK

{serve_page('index.html')}
"""
        elif "POST /login" in message:
            # Divide a mensagem recebida em linhas
            lines = message.split("\r\n")
            login_attempt = lines[-1] # ultima linha contem a tentiva de login no seguinte formato "user=usuario&password=senha"
            # Verifica o usuário e a senha
            if login_attempt == f"user={USER}&password={PASSWORD}":
                authenticated = True
            # Redireciona para a página de sucesso ou falha
            if authenticated:
                response = f"""HTTP/1.1 200 OK

{serve_page('success.html')}
"""
            else:
                response = f"""HTTP/1.1 200 OK

{serve_page('error.html')}
"""
        elif "POST /logout" in message:
            # Realize as ações de logout, como redefinir o estado de autenticação
            authenticated = False
            # Redirecione de volta para a página de login
            response = """HTTP/1.1 302 Found
Location: /
"""
        # Envie a resposta para o navegador
        connectionSocket.sendall(response.encode())
        connectionSocket.close()
    except IOError:
        pass
serverSocket.close()
sys.exit()
