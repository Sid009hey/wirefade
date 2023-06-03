import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # Error occurred while receiving message
            break

def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def start_chat():
    host = '192.168.1.225'  # or '127.0.0.1'
    port = 8009  # Choose a suitable port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive the initial prompt for username
    username_prompt = client_socket.recv(1024).decode('utf-8')
    print(username_prompt, end=' ')
    username = input("➡️ ")
    print("Chat Started, Type Below and press `Enter` \n⬇️")
    client_socket.send(username.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

start_chat()

