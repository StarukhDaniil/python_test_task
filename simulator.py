from pymavlink import mavutil

class Simulator:
    def __init__(self, tlog_path, port):
        self.__log_connection = mavutil.mavlink_connection(tlog_path)
        self.__handler_connection = mavutil.mavlink_connection(f"tcpout:127.0.0.1:{port}")
    
    def simulate(self):
        while True:
            msg = self.__log_connection.recv_match()
            if msg is None:
                break;
            raw_bytes = msg.get_msgbuf()
            self.__handler_connection.write(raw_bytes)