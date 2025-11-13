from pymavlink import mavutil
import multiprocessing
import argparse

import simulator
import handler

def main():
    argParser = argparse.ArgumentParser(description="Sending messages and hadnling them")
    argParser.add_argument("tlog", help="Path to .tlog file")
    args = argParser.parse_args()

    reciever_conn, sender_conn = multiprocessing.Pipe()

    simulatorProcces = multiprocessing.Process(target=simulator.runSim, args=(args.tlog, sender_conn,))
    simulatorProcces.start()

    handler.runHandler(reciever_conn)

    simulatorProcces.join()

if __name__ == "__main__":
    main()