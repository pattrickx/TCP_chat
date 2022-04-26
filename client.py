import socket
import threading


class client:
    def __init__(self,host,port) -> None:
        self.host = host
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_open = True
    def start(self):
        self.sock.connect((HOST, PORT))
        thread_received_message = threading.Thread(target=self.handle_received_message)
        thread_received_message.start()
        thread_user = threading.Thread(target=self.handle_user)
        thread_user.start()

    def handle_received_message(self):
        while self.conn_open:
            print(self.conn_open)
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
                print(data["msg"])

    def login(self):
        user = input('Digite o seu nome de usuario: ')
        password = input('Digite sua Senha :')
        
        msg = {"type":"login", "user":user , "password":password}
        self.sock.sendall(str(msg).encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        if data:
            data = eval(data)
            if data["type"]== "status" and data['msg']=="OK":
                return True
        self.conn_open = False
        self.sock.close()
        return False

    def logout(self):
        msg = {"type":"logout"}
        self.sock.sendall(str(msg).encode('utf-8'))
        self.sock.close()

    def handle_user(self):
        if not self.login():
            print("não foi possivel efetuar o login")
        else:
            while self.conn_open:
                try:
                    destination = input('Digite o nome do usuario de destino ou all se for para todos: ')
                    mensagem = input('Digite uma mensagem a ser enviada ao servidor: ')
                    if destination == "" or mensagem == "":
                        self.logout()
                        break
                    msg = {"type":"msg", "user":destination, "msg":mensagem}
                    # s.sendall(mensagem.encode('utf-8')) # manda o array de bytes da string
                    self.sock.sendall(str(msg).encode('utf-8')) # manda o array de bytes da string
                except KeyboardInterrupt:
                    print(" ")
                    print('Encerrando cliente')
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