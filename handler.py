from pymavlink.dialects.v20 import common as mavlink_dialect
import csv
import socket
import time

# how often to write csv
RECV_CYCLES_FOR_LOG = 4

class Handler:
    def __init__(self, port):
        # port validation
        if port > 65535 or port < 0:
            raise ValueError("Port has to be between 0 and 65535")
        
        # buffer for collecting bytes
        self.__bytes_received = bytearray()

        # creating parser
        self.__mav = mavlink_dialect.MAVLink(file=None)

        # establishing connection with simulator
        self.__simulator_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__simulator_connection.bind(('127.0.0.1', port))

        # dictionaries for csv
        self.__file_handlers = {}
        self.__csv_writers = {}
    
    def run(self):
        # waiting for simulator to join
        self.__simulator_connection.listen()
        conn, addr = self.__simulator_connection.accept()

        # counter for calling self.__write_csv() from time to time
        counter = 0
        while True:
            # reading bytes from simulator
            chunk = conn.recv(1024)

            if not chunk:
                break

            self.__bytes_received.extend(chunk)
            
            counter += 1
            if counter == RECV_CYCLES_FOR_LOG:
                self.__write_csv()
                self.__bytes_received.clear()
                counter = 0

        # one additional time if counter didn't reach RECV_CYCLES_FOR_LOG
        self.__write_csv()
        conn.close()

    def __write_csv(self):
        msg_list = self.__mav.parse_buffer(self.__bytes_received)
        
        if msg_list is None:
            return
        try:
            for msg in msg_list:
                msg_type = msg.get_type()
                if msg_type not in self.__csv_writers:
                    self.__create_csv(msg)

                row = [time.time()] + list(msg.to_dict().values())
                
                writer = self.__csv_writers[msg_type]
                writer.writerow(row)
        except Exception as e:
            print(f"Error while logging: {e}")

    def __create_csv(self, msg):
        msg_type = msg.get_type()

        try:
            file = open(f"./csv/{msg_type}.csv", 'w', newline='', encoding='utf-8')
        except Exception as e:
            print(f"Error while opening or creating .csv log file: {e}")
            

        csv_writer = csv.writer(file)

        headers = ['timestamp'] + msg.get_fieldnames()
        csv_writer.writerow(headers)

        # saving handlers and writers in dictionaries
        self.__csv_writers[msg_type] = csv_writer
        self.__file_handlers[msg_type] = file
    
    def __del__(self):
        # closing file handlers
        for fh in self.__file_handlers.values():
            fh.close()


def runHandler(port):
    handler = Handler(port)
    handler.run()