from multiprocessing.connection import Connection
from pymavlink import mavutil
import socket

class Simulator:
    def __init__(self, tlog_path, port: int):
        if port > 65535 or port < 0:
            raise ValueError("Port has to be between 0 and 65535")
        
        self.__port = port

        self.__tlog = mavutil.mavlink_connection(tlog_path)
        self.__handler_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        self.__handler_connection.connect(('127.0.0.1', self.__port))
        while True:
            msg = self.__tlog.recv_match()

            # if all data from .tlog have been read, then break the loop
            if not msg:
                break

            # bytes from message
            raw_msg = msg.get_msgbuf()

            try:
                # sending raw data from .tlog
                self.__handler_connection.sendall(raw_msg)
            except BrokenPipeError:
                print("Error: broken pipe")
                
    
    def __del__(self):
        # closing file
        self.__tlog.close()
        
        # closing connection
        self.__handler_connection.close()
    
def runSim(tlog_path, port):
    simulator = Simulator(tlog_path, port)
    simulator.run()