from socket import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Função para carregar a chave pública do servidor
def load_public_key():
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

serverName = "192.168.10.186"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Carrega a chave pública do servidor
server_public_key = load_public_key()

sentence = input("Input lowercase sentence: ")

# Criptografa a mensagem com a chave pública do servidor
encrypted_sentence = server_public_key.encrypt(
    bytes(sentence, "utf-8"),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

clientSocket.send(encrypted_sentence)

# Recebe a mensagem criptografada do servidor
encrypted_response = clientSocket.recv(1024)

# Decriptografa a resposta usando a chave privada do cliente (implementar a lógica de carregamento e decriptografia da chave privada do cliente)

clientSocket.close()
