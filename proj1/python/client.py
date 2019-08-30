import socket 
  
def readlines(sock, buffer_size=2048, delim='\n'):
    """
    Read data from socket until connection is closed,
    and supply a generator interface.
    """
    buf = ''
    data = True
    while data:
        data = sock.recv(buffer_size)
        buf += data.decode()

        while buf.find(delim) != -1:
            line, buf = buf.split(delim, 1)
            yield line
    return

def Main(): 
    host = '127.0.0.1'
    port = 7777
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect((host,port)) 
    print('Client conected.')
    while True: 
  
     for line in readlines(s):
        print('New line: ' + line)

    s.close() 
  
if __name__ == '__main__': 
    Main() 