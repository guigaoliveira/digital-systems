import sys
import os
import serial
import threading
import socket
import logging
import signal

log = logging.getLogger('brigde')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)


class Bridge:
    def __init__(self, serial, socket):
        self.serial = serial
        self.socket = socket

    def shortcut(self):
        """ conecta a porta serial a porta tcp e copia tudo de uma para outra """
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.writer()

    def reader(self):
        """copia da serial para o socket"""
        while self.alive:
            try:
                data = self.serial.read(1) # lê o primeiro byte
                n = self.serial.inWaiting()  # espera se existe mais dados a serem lidos
                if n:
                    data = data + self.serial.read(n) # lê mais n bytes
                if data:
                    self.socket.sendall(data) # envia tudo via TCP
            except socket.error as msg:
                log.error(msg) # provavelmente uma desconexão
                break
        self.alive = False

    def writer(self):
        """copia do socket para a serial"""
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.serial.write(data)  # get a bunch of bytes and send them
            except socket.error as msg:
                log.error(repr(msg))
                break
            except Exception as e:
                log.critical(repr(e))
                break
        self.alive = False
        self.thread_read.join()

    def stop(self):
        """Stop copying"""
        if self.alive:
            self.alive = False
            self.thread_read.join()

if __name__ == '__main__':
    ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

    log.info("Serial -> TCP/IP & TCP/IP -> Serial (Ctrl-C para sair)")

    try:
        if(ser.isOpen() == False):
            ser.open()
    except serial.SerialException as e:
        log.fatal(f"Não foi possível abrir a porta serial {ser.portstr}: {e}")
        sys.exit(1)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(('', 7777))
    srv.listen(1)

    def signal_handler(signal, frame):
        try:
            srv.close()
        except Exception as e:
            log.warning(repr(e))
        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while 1:
        try:
            log.info("Esperando por alguma conexão...")
            connection, addr = srv.accept()
            address, port = addr
            log.info('Conectando a tcp://{0}:{1}'.format(address, port))
            r = Bridge(ser, connection)
            r.shortcut()
        except socket.error as msg:
            log.error(msg)
        finally:
            try:
                connection.close()
                log.info('Desconectando...')
            except NameError:
                pass
            except Exception as e:
                log.warning(repr(e))