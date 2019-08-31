import socket
from pynput import keyboard
import threading 

host = '127.0.0.1'
port = 7777

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.connect((host,port)) 
print(f'Cliente conectado com sucesso, no endereço e porta: {host}:{port}')

def input_to_client(sock):
    def on_press(key):
        try:
            print(f'Você pressionou {key}')
            if(key.char == '1' or key.char == '2' or key.char == '3'):
                sock.send(str.encode(key.char))
        except AttributeError:
            print(f'Caracter especial {key} pressionado')
    return on_press

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def readlines(sock, buffer_size=2048, delim='\n'):
    buf = ''
    data = True
    while data:
        data = sock.recv(buffer_size)
        buf += data.decode()

        while buf.find(delim) != -1:
            line, buf = buf.split(delim, 1)
            yield line
    return

def Main(sock): 
    while True: 
  
     for line in readlines(s):
        print('Nova linha: ' + line)

    sock.close() 

def test(sock):
    with keyboard.Listener(
            on_press=input_to_client(sock),
            on_release=on_release) as listener:
        listener.join()
if __name__ == '__main__': 
     thread1 = threading.Thread(target=Main, args=(s, ))
     thread1.start()
     thread2 = threading.Thread(target=test, args=(s, ))
     thread2.start()