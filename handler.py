from pymavlink.dialects.v20 import common as mavlink_dialect
import csv
import socket
import time

class Handler:
    def __init__(self, port):
        # establishing connection with simulator
        # self.__simulator_connection = mavutil.mavlink_connection(f"tcpin:127.0.0.1:{port}")
        self.__bytes_received = bytearray()
        self.__mav = mavlink_dialect.MAVLink(file=None)

        self.__simulator_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__simulator_connection.bind(('127.0.0.1', port))

        self.__file_handlers = {}
        self.__csv_writers = {}
    
    def run(self):
        self.__simulator_connection.listen()
        conn, addr = self.__simulator_connection.accept()
        # asd = False
        counter = 0
        while True:
            # reading bytes from simulator
            chunk = conn.recv(1024)

            if not chunk:
                break

            # if not asd:
            #     asd = True
            #     print(chunk)

            self.__bytes_received.extend(chunk)
            
            counter += 1
            if counter == 4:
                self.__write_csv()
                self.__bytes_received.clear()
                counter = 0

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

                writer = self.__csv_writers[msg_type]
                row = [time.time()] + list(msg.to_dict().values())

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
        self.__csv_writers[msg_type] = csv_writer
        self.__file_handlers[msg_type] = file
    
    def __del__(self):
        for fh in self.__file_handlers.values():
            fh.close()


def runHandler(port):
    handler = Handler(port)
    handler.run()