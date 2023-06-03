import socket
import threading

def handle_client(client_socket, client_username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast_message("✅ " + client_username + " : " + message) 
        except:
            # Error occurred while receiving message
            break

def broadcast_message(message):
    for client_socket, client_username in clients:
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            # Error occurred while sending message
            remove_client(client_socket)

def remove_client(client_socket):
    for i, (socket, username) in enumerate(clients):
        if socket == client_socket:
            clients.pop(i)
            break

def start_chat():
    host = '192.168.1.225'  # or '127.0.0.1'
    port = 8009  # Choose a suitable port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Chatroom server started on {}:{}".format(host, port))

    while True:
        client_socket, client_address = server_socket.accept()

        # Prompt the client to enter a username
        client_socket.send("Enter your username: ".encode('utf-8'))
        client_username = client_socket.recv(1024).decode('utf-8')

        clients.append((client_socket, client_username))

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_username))
        client_thread.start()

clients = []

start_chat()

