import socket
import threading

def handle_connection(con):
    while True:
        try:
            con.recv(1024)  # wait for client to send data
            con.send(b"+PONG\r\n")
        except ConnectionError:
            break
        con.close()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()  # wait for client
        print(f"Connected to {address}")
        threading.Thread(target=handle_connection, args=(connection)).start()


if __name__ == "__main__":
    main()