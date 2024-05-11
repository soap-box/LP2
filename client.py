import socket
import secrets



def diffie_hellman_step(secret, p, g):
    return pow(g, secret, p)


def main():
    host = 'localhost'
    port = 5005
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    
    p = int(input("Enter a prime number p: "))
    g = int(input("Enter a base  prime number g: "))
    
    
    client.send(str(p).encode())
    client.send(str(g).encode())
    
    
    client_secret = secrets.randbelow(p)
    client_public = diffie_hellman_step(client_secret, p, g)
    # print("Public number by user1:", client_public)
    client.send(str(client_public).encode())
    
   
    server_public = int(client.recv(1024).decode())
    shared_secret = pow(server_public, client_secret, p)
    print("Final shared key:", shared_secret)
    client.close()

if __name__ == "__main__":
    main()
