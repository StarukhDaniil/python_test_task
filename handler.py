from pymavlink import mavutil
import socket
import csv
from multiprocessing.connection import Connection

class Handler:
    def __init__(self, conn: Connection):
        # establishing connection with simulator
        self.__connection = conn
    
    def run(self):
        while self.__connection.poll(1):
            # reading bytes from simulator
            chunk = self.__connection.recv()
            
            if chunk is None:
                break
            print(chunk)

def runHandler(port):
    handler = Handler(port)
    handler.run()