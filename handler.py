from pymavlink import mavutil
import csv

class Handler:
    def __init__(self, port: int):
        # port validation
        if port < 0 or port > 65535:
            raise ValueError("port has to be between 0 and 65535")
        
        self.__simulator_connection = mavutil.mavlink_connection(f"tcpin:127.0.0.1:{port}")
    
    def run(self):
        while True:
            msg = self.__simulator_connection.recv_match(blocking=True)
            print(msg)

def runHandler(port):
    handler = Handler(port)
    handler.run()