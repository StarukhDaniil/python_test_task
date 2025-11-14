from pymavlink import mavutil
import multiprocessing
import argparse
import time
import simulator
import handler
import os

def main():
    # parsing path to .tlog
    argParser = argparse.ArgumentParser(description="Sending messages and hadnling them")
    argParser.add_argument("tlog", help="Path to .tlog file")
    args = argParser.parse_args()

    # if user doesn't have csv/ directory, then create it
    os.makedirs("./csv", exist_ok=True)

    reciever_conn, sender_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=handler.runHandler, args=(2000,))
    p.start()

    # waiting for handler to set up connection
    time.sleep(3)

    simulator.runSim(args.tlog, 2000)

    p.join()

    print("Logs are in the csv directory")

if __name__ == "__main__":
    main()