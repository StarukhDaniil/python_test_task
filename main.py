from pymavlink import mavutil
import multiprocessing
import argparse

import simulator
import handler

def main():
    argParser = argparse.ArgumentParser(description="Sending messages and hadnling them")
    argParser.add_argument("tlog", help="Path to .tlog file")
    args = argParser.parse_args()

    port = 2000

    simulatorProcces = multiprocessing.Process(target=simulator.runSim, args=(args.tlog, port,))
    simulatorProcces.start()

    handler.runHandler(port)

    simulatorProcces.join()

if __name__ == "__main__":
    main()