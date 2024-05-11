import socket
import secrets


def diffie_hellman_step(secret, p, g):
    return pow(g, secret, p)


def main():
    host = 'localhost'
    port = 5005
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("Server is listening on port:", port)
    
    client_socket, addr = server.accept()
    print("Connected to client at address:", addr)
    
    # Receive p and g from client
    p = int(client_socket.recv(1024).decode())
    g = int(client_socket.recv(1024).decode())
    
    # Generate server's secret and public values
    server_secret = secrets.randbelow(p)
    server_public = diffie_hellman_step(server_secret, p, g)
    # print("Public number by user2:", server_public)
    client_socket.send(str(server_public).encode())
    
    # Receive client's public value
    client_public = int(client_socket.recv(1024).decode())
    shared_secret = pow(client_public, server_secret, p)
    
    
    print("Final shared key:", shared_secret)
    client_socket.close()

if __name__ == "__main__":
    main()
