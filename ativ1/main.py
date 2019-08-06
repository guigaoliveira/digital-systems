import serial
import time

ser = serial.Serial('COM4', 9600) 

def read_data(): 
    reading = str(ser.readline(), "utf-8")
    print("Dados lido:", reading)

def write_data(data): 
    ser.write(data)

data_to_write = 0 
while True:
    print("Enviando: ", data_to_write)
    write_data(data_to_write) # envia os dados pela serial
    data_to_write = int(not data_to_write) # alterna o estado do dado a ser enviado (0 ou 1) 
    time.sleep(0.4)
    print("Lendo...")
    read_data() # ler os dados da serial
