import socket 
from _thread import *
import threading 
import time
import serial

lock = threading.Lock() 
clients = []
ser = serial.Serial('', 9600) 

serialData = ""
def clientThreadHandle(c): 
    global serialData
    while True: 
        if serialData:
            c.send(str.encode(serialData)) 
            serialData = ""
    c.close() 
  
def getSerialDataThreadHandle(): 
    global serialData
    while True: 
        time.sleep(0.5)
        serialData = str(ser.readline(), "utf-8")
  
def Main(): 
    host = "" 
    port = 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port)) 
    print("socket binded to port", port) 
    s.listen(5) 
    print("socket is listening") 
    while True: 
        c, addr = s.accept() 
        clients.append(c)
        lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
        start_new_thread(clientThreadHandle, (c,)) 
        start_new_thread(getSerialDataThreadHandle, ())
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 