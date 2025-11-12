from pymavlink import mavutil
import time

def f():
    print("simulator started")
    time.sleep(1)
    print("simulator ended")

# def simulate(tlog_path):
#     log = mavutil.mavlink_connection(tlog_path)

#     while True:
#         msg = log.recv_match()
#         if msg is None:
#             break