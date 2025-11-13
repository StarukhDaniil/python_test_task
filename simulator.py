from pymavlink import mavutil

class Simulator:
    def __init__(self, tlog_path, port: int):
        # port validation
        if port < 0 or port > 65535:
            raise ValueError("port has to be between 0 and 65535")
        
        # establishing connection with .tlog and handler
        self.__log_connection = mavutil.mavlink_connection(tlog_path)
        self.__handler_connection = mavutil.mavlink_connection(f"tcp:127.0.0.1:{port}")
    
    def run(self):
        while True:
            # getting one of the .tlog messages
            msg = self.__log_connection.recv_match()

            if msg is None:
                break;
            
            # sending raw data from msg
            raw_bytes = msg.get_msgbuf()
            self.__handler_connection.write(raw_bytes)
    
def runSim(tlog_path, port: int):
    simulator = Simulator(tlog_path, port)
    simulator.run()