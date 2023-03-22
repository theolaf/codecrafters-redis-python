import socket
import threading

def parse_response(msg):
    decoded = msg.decode("utf-8")
    if len(decoded) == 0:
        return None
    return decoded.split('\r\n')

def write_reply(input):
    if input is None:
        return None
    command = input[2].lower()
    if command == "ping":
        return "+PONG\r\n"
    if command == "echo":
        return f"${len(input[4])}\r\n{input[4]}\r\n"
    else:
        return None

def handle_connection(con):
    while True:
        try:
            msg = con.recv(1024)
            resp = parse_response(msg)
            reply = write_reply(resp)
            if reply is not None:
                con.send(str.encode(reply))
        except ConnectionError:
            break

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        print(f"Connected to {address}")
        threading.Thread(target=handle_connection, args=[connection]).start()


if __name__ == "__main__":
    main()