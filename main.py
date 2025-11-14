from pymavlink import mavutil
import multiprocessing
import argparse
import time
import simulator
import handler

def main():
    argParser = argparse.ArgumentParser(description="Sending messages and hadnling them")
    argParser.add_argument("tlog", help="Path to .tlog file")
    args = argParser.parse_args()

    reciever_conn, sender_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=handler.runHandler, args=(2000,))
    p.start()
    time.sleep(3)
    simulator.runSim(args.tlog, 2000)

    p.join()

if __name__ == "__main__":
    main()