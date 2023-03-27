import socket
import threading

class RedisServer:
    # constructor, getters and setters
    def __init__(self, address=(("localhost", 6379))):
        self.db = {}
        self.server_socket = socket.create_server(address, reuse_port=True)
    
    def set(self, key, value):
        self.db[key] = value
        print(f"Set {key}: {value}")

    def get(self, key):
        return self.db.get(key)
    
    # connection handling
    def event_loop(self):
        while True:
            connection, address = self.server_socket.accept()
            print(f"Connected to {address}")
            threading.Thread(target=self.handle_connection, args=[connection]).start()

    def handle_connection(self, con):
        while True:
            try:
                msg = con.recv(1024)
                resp = self.parse_response(msg)
                reply = self.write_reply(resp)
                if reply is not None:
                    con.send(str.encode(reply))
            except ConnectionError:
                break
    
    # parsing and response logic
    def parse_response(self, msg):
        decoded = msg.decode("utf-8")
        if len(decoded) == 0:
            return None
        return decoded.split('\r\n')

    def write_reply(self, input):
        if input is None:
            return None
        command = input[2].lower()
        if command == "ping":
            return "+PONG\r\n"
        if command == "echo":
            return f"${len(input[4])}\r\n{input[4]}\r\n"
        if command == "set":
            self.set(input[4], input[6])
            return "+OK\r\n"
        if command == "get":
            value = self.get(input[4])
            return f"${len(value)}\r\n{value}\r\n" if value else "$-1\r\n"
        else:
            return None

def main():
    redis = RedisServer()
    redis.event_loop()

if __name__ == "__main__":
    main()