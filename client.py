import socket
import threading
import time

class client:
    def __init__(self,host,port) -> None:
        self.host = host
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_open = True
    def start(self):
        self.sock.connect((HOST, PORT))
        if not self.login():
            print("Não foi possivel efetuar o login")
        else:
            thread_user = threading.Thread(target=self.handle_user)
            thread_user.start()

            thread_received_message = threading.Thread(target=self.handle_received_message)
            thread_received_message.start()

    def handle_received_message(self):
        while self.conn_open:
            data = self.sock.recv(1024).decode('utf-8')
            if not data:
                self.sock.close()
                self.conn_open = False
                break
            data = eval(data)
            if data["type"]=="msg":
                print(" ")
                print(data["msg"])
            if data["type"]=="status":
                print(" ")
                print(f"STATUS: {data['msg']}")

    def login(self):
        try:
            user = input('Digite o seu nome de usuario: ')
            password = input('Digite sua Senha :')
            
            msg = {"type":"login", "user":user , "password":password}
            self.sock.sendall(str(msg).encode('utf-8'))
            data = self.sock.recv(1024).decode('utf-8')
            if data:
                data = eval(data)
                if data["type"]== "status" and data['msg']=="OK":
                    return True
            self.sock.close()
            return False
        except KeyboardInterrupt:
            self.sock.close()
        except Exception as E:
            print(E)
            self.sock.close()

    def logout(self):
        msg = {"type":"logout"}
        self.conn_open = False
        self.sock.sendall(str(msg).encode('utf-8'))
        self.sock.close()
    def handle_msg(self,mensagem):
        if mensagem.startswith("SEND"):
            destination = mensagem.split(" ")[1]
            mensagem = mensagem.replace(f"SEND {destination} ","")
            msg = {"type":"msg", "user":destination, "msg":mensagem}
            # s.sendall(mensagem.encode('utf-8')) # manda o array de bytes da string
            self.sock.sendall(str(msg).encode('utf-8'))
        else:
            msg = {"type":"msg", "user":"all", "msg":mensagem}
            # s.sendall(mensagem.encode('utf-8')) # manda o array de bytes da string
            self.sock.sendall(str(msg).encode('utf-8'))
        
    def handle_user(self):
        while self.conn_open:
            try:
                mensagem = input()
                if mensagem == "":
                    self.logout()
                    break
                self.handle_msg(mensagem)
            except KeyboardInterrupt or Exception:
                print(" ")
                print('Encerrando cliente')
                self.sock.sendall(str({"type":"logout"}).encode('utf-8'))
                self.sock.close()
                break


    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))  # faz a conexão
        
    #     thread_received_message = threading.Thread(target=handle_received_message, args=(s,))
    #     thread_received_message.start()
    #     thread_user = threading.Thread(target=handle_user, args=(s,))
    #     thread_user.start()
HOST = 'localhost' # servidor que quero conectar
PORT = 1234

if __name__ == '__main__':
    c = client(HOST,PORT)
    c.start()