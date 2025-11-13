from pymavlink import mavutil
import multiprocessing

import simulator
import handler

if __name__ == "__main__":
    port = 2000

    simulatorProcces = multiprocessing.Process(target=simulator.runSim, args=(port,))
    simulatorProcces.start()

    handler.runHandler(port)

    simulatorProcces.join()