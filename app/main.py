import socket
import threading

class RedisHandler:
    def __init__(self):
        self.db = {}
    
    def set(self, key, value):
        self.db[key] = value
        print(f"Set {key}: {value}")

    def get(self, key):
        return self.db.get(key)
    
def parse_response(msg):
    decoded = msg.decode("utf-8")
    if len(decoded) == 0:
        return None
    return decoded.split('\r\n')

def write_reply(input, redis):
    if input is None:
        return None
    command = input[2].lower()
    if command == "ping":
        return "+PONG\r\n"
    if command == "echo":
        return f"${len(input[4])}\r\n{input[4]}\r\n"
    if command == "set":
        redis.set(input[4], input[6])
        return "+OK\r\n"
    if command == "get":
        value = redis.get(input[4])
        return f"${len(value)}\r\n{value}\r\n" if value else "$-1\r\n"
    else:
        return None

def handle_connection(con, redis):
    while True:
        try:
            msg = con.recv(1024)
            resp = parse_response(msg)
            reply = write_reply(resp, redis)
            if reply is not None:
                con.send(str.encode(reply))
        except ConnectionError:
            break

def main():
    redis = RedisHandler()
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        print(f"Connected to {address}")
        threading.Thread(target=handle_connection, args=[connection, redis]).start()


if __name__ == "__main__":
    main()