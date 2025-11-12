from pymavlink import mavutil
import multiprocessing

import simulator
import handler

if __name__ == "__main__":
    simulatorProcces = multiprocessing.Process(target=simulator.f)
    handlerProcess = multiprocessing.Process(target=handler.f)

    simulatorProcces.start()
    handlerProcess.start()

    simulatorProcces.join()
    handlerProcess.join()