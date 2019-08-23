# Import socket module 
import socket 
  
  
def Main(): 
    host = '127.0.0.1'
    port = 9000
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host,port)) 
    print('Cliente conectado.')
    while True: 
  
        data = s.recv(1024) 
        if data: 
            print('Received from the server:',str(data.decode('ascii'))) 
    s.close() 
  
if __name__ == '__main__': 
    Main() 