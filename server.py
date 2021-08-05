import socket
import threading
import sys
import json

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost" #TODO CHECK HOW TO READ THIS VALUE
        self.port = 15000
        self.server_ip = socket.gethostbyname(self.server)
        self.currentId = 0
        self.pos = {}
        

    def check_server(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))

    def threaded_client(self, conn):
        conn.send(str.encode(str(self.currentId)))
        self.currentId += 1
        
        while True:
            try:
                data = conn.recv(2048)

                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                
                reply = json.loads(data.decode('utf-8'))
                if "exit" in reply:
                    self.pos.pop(reply["exit"])
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    self.pos.update(reply)
                    reply = json.dumps(self.pos)
                    conn.sendall(str.encode(reply))
            except Exception as exc:
                print(str(exc))
                break

        print("Connection Closed")
        conn.close()
    
    def start(self, players):
        self.check_server()
        self.s.listen(players)
        while True:
            try:
                print("Waiting for a connection")
                conn, addr = self.s.accept()
                print("Connected to: ", addr)
                t = threading.Thread(target=self.threaded_client, args=(conn, ))
                t.start()
            except KeyboardInterrupt:
                self.s.close()
                sys.exit()


if __name__ == "__main__":
    server = Server()
    server.start(2)