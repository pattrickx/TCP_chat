import socket
from threading import Thread
class WebServer:

    def __init__(self, users, address='0.0.0.0', port=1234):
        self.users =users
        self.port = port
        self.address = address
        self.clients = []

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            
            s.listen(10)
            
            while True:
                try:
                    print(f"Aguardando novas conexões...")
                    conn, addr = s.accept()

                    thread = Thread(target=self.client_handle, args=(conn, addr)) # "," é pra saber que é o fim da tupla
                    thread.start()
                except KeyboardInterrupt:
                    print("Encerrando servidor.")
                    s.close()
                    break  
    def send_status(self,conn,msg):
        data_status = {"type":"status", "msg":msg}
        conn.sendall(str(data_status).encode('utf-8'))

    def send_to_all_clients(self,client,msg):
        if len(self.clients)>1:
            for to_client in self.clients:
                if to_client["user"] != client["user"]:
                    data = {"type":"msg", "msg":f"{client['user']} disse: {msg}"}
                    to_client["conn"].sendall(str(data).encode('utf-8'))
            self.send_status(client["conn"],"Mensagem enviada com sucesso")
        self.send_status(client["conn"],"Nenhum cliente Online")

    def send_to_user(self,client,to_user,msg):
        if len(self.clients)>1:
            for to_client in self.clients:
                if to_client['user']==to_user:
                    data = {"type":"msg", "msg":f"{client['user']} disse: {msg}"}
                    to_client["conn"].sendall(str(data).encode('utf-8'))
                    self.send_status(client["conn"],"Mensagem enviada com sucesso")
        self.send_status(client["conn"],"Usuario offline")
    
    def client_handle(self, conn, addr):

        client = {"conn": conn, "addr": addr, "user":""}
        with conn:
            data = eval(conn.recv(1024).decode('utf-8'))

            # Login
            if data['type'] == "login" and data['user'] and data["password"]:
                if data['user'] in self.users["user"] and data["password"] == self.users["password"][self.users["user"].index(data['user'])]:
                    client["user"] = data['user']
                    self.clients.append(client)
                    self.send_status(conn,"OK")
                else:
                    self.send_status(conn,"ERROR")
                    conn.close()
                    return 0
            else:
                self.send_status(conn,"ERROR")
                conn.close()
                return 0

            print(f'Conectado a {addr}')
            print(" ")
            while True:
                data = eval(conn.recv(1024).decode('utf-8'))
                print(f"Mensagem recebida de {addr}: {data}")
                if not data: break
                if data['type']=="logout":
                    conn.close()
                    self.clients.pop(self.clients.index(client))
                    break
                if data['type']=="msg":
                    if data["user"]=="all":
                        self.send_to_all_clients(client,data["msg"])
                    else:
                        self.send_to_user(client,data["user"],data["msg"])

users = {"user":["patrick","test"],"password":["1234","4321"]}
if __name__ == '__main__':
    server = WebServer(users)
    server.start()

