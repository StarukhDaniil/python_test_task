import multiprocessing
from multiprocessing.connection import Connection

class Simulator:
    def __init__(self, tlog_path, conn: Connection):
        # open .tlog for reading as binary
        self.__tlog = open(tlog_path, "rb")

        # saving connection with handler
        self.__connection = conn
    
    def run(self):
        while True:
            # getting 1024 bytes of .tlog
            raw_chunk = self.__tlog.read(1024)

            # if all data from .tlog have been read, the break the loop
            if len(raw_chunk) == 0:
                break

            # sending raw data from .tlog
            self.__connection.send(raw_chunk)
    
    def __del__(self):
        # closing file
        if not self.__tlog.closed:
            self.__tlog.close()
        
        # closing connection
        if not self.__connection.closed:
            self.__connection.close()
    
def runSim(tlog_path, conn):
    simulator = Simulator(tlog_path, conn)
    simulator.run()