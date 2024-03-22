from socket import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Função para carregar a chave privada do servidor
def load_private_key():
    with open("server_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Se a chave privada for protegida por senha, insira-a aqui.
            backend=default_backend()
        )
    return private_key

serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)

print("TCP Server\n")

connectionSocket, addr = serverSocket.accept()

# Carrega a chave privada do servidor
server_private_key = load_private_key()

# Recebe a mensagem criptografada do cliente
encrypted_sentence = connectionSocket.recv(65000)

# Decriptografa a mensagem usando a chave privada do servidor
sentence = server_private_key.decrypt(
    encrypted_sentence,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

received = str(sentence, "utf-8")
print("Received From Client: ", received)

# Processamento (por exemplo, transformar em maiúsculas)
response = received.upper()

# Criptografa a resposta com a chave pública do cliente antes de enviá-la (implementar a lógica de carregamento e criptografia com a chave pública do cliente)

connectionSocket.close()
