import datetime
from multiprocessing import log_to_stderr
import time
import threading
from collections import deque


################################################################################
#   Handle all connections and rights for the server
################################################################################
class MachineMotor:
    name = None
    priority = -1
    period = -1
    execution_time = -1
    need = -1
    product = None

    ############################################################################
    def __init__(self, name, priority, period, need, product, execution_time):
        self.name = name
        self.priority = priority
        self.need = need
        self.period = period
        self.execution_time = execution_time
        self.product = product

    ############################################################################
    def run(self):
        global tank, stock_motor, stock_wheel, executing
        while stock_wheel / 4 >= stock_motor:
            executing = True
            print(self.name + " producing 1 " + self.product)
            time.sleep(self.execution_time)
            tank -= self.need
            stock_motor += 1

            print(self.name + " has finished producing " + self.product + " " + datetime.datetime.now().strftime("%H:%M:%S"))
            print("**** motors = ", str(stock_motor) + " wheels = " + str(stock_wheel) + " *****")
            executing = False
            time.sleep(self.period)
            return


################################################################################
#   Handle all connections and rights for the server
################################################################################
class MachineWheel:
    name = None
    priority = -1
    period = -1
    execution_time = -1
    need = -1
    product = None

    ############################################################################
    def __init__(self, name, priority, period, need, product, execution_time):
        self.name = name
        self.priority = priority
        self.need = need
        self.period = period
        self.execution_time = execution_time
        self.product = product

    ############################################################################
    def run(self):
        global tank, stock_motor, stock_wheel, executing
        while stock_wheel % 4 <= stock_motor:
            executing = True
            print(self.name + " producing 1 " + self.product)
            time.sleep(self.execution_time)
            tank -= self.need
            stock_wheel += 1

            print(self.name + " has finished producing " + self.product + " " + datetime.datetime.now().strftime("%H:%M:%S"))
            print("**** motors = ", str(stock_motor) + " wheels = " + str(stock_wheel) + " *****")
            executing = False
            time.sleep(self.period)
            return

################################################################################
#   Handle all connections and rights for the server
################################################################################
class Pump:
    name = None
    priority = -1
    period = -1
    execution_time = -1
    amount = -1

    ############################################################################
    def __init__(self, name, priority, period, amount, execution_time):
        self.name = name
        self.priority = priority
        self.amount = amount
        self.period = period
        self.execution_time = execution_time

    ############################################################################
    def run(self):
        global tank, executing
        while tank < tank_limit:
            print(self.name + " started pumping " + str(self.amount))
            tank += self.amount
            time.sleep(self.execution_time)
            print(self.name + " has finished pumping " + " " + datetime.datetime.now().strftime("%H:%M:%S"))
            print("**** tank is at " + str(tank) + " ****")
            executing = True
            time.sleep(self.period)
            return


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':

    global tank, stock_wheel, stock_motor, tank_limit, executing
    tank = 0
    stock_wheel = 0
    stock_motor = 0
    tank_limit = 50
    executing = False

    last_execution = datetime.datetime.now()

    # Instanciation of task objects
    task_list = []

    task_list.append \
        (Pump(name="Pump 1", priority=1, period=5, amount=10, execution_time=2))

    task_list.append \
        (Pump(name="Pump 2", priority=1, period=15, amount=20, execution_time=3))
    task_list.append \
        (MachineMotor(name="Machine 1", priority=1, period=5, need=25, product="motor", execution_time=5))
    task_list.append \
        (MachineWheel(name="Machine 2", priority=1, period=5, need=5, product="wheel", execution_time=3))

    # Global scheduling loop
    while 1:

        for currentTask in task_list:
            currentTask.run()
