from global_variables import run_command
import sys
from random import random
from time import sleep
from multiprocessing import Pool, cpu_count, Value

"""
Causes CPUs to heat up and fans to start spinning
This can be regulated or unregulated
"""

targetTemp = 66
currentTemp = Value('f', 0)

def get_CPU_tempurate():
    #Requires root permission
    with open('upassword.txt', 'r') as passwordFile:
        password = passwordFile.readline()[:-1]
        CPUtemperatureReadings = run_command(f"""echo {password} | sudo -S powermetrics -n 3 | grep -i 'CPU die temperature' | cut -d' ' -f4""").decode()
        CPUtemperatureReadings = CPUtemperatureReadings.split('\n')
        CPUtemperatureReadings = CPUtemperatureReadings[:3]
        average = 0
        print(CPUtemperatureReadings)
        for temp in CPUtemperatureReadings:
            average += float(temp)
        average /= len(CPUtemperatureReadings)

        return average


#Will revv up the CPU whenever it's temperature is less than the target temperature
def rev_the_engines(i):
    number = 0
    while True:
        if currentTemp.value > targetTemp:
            sleep(1 + random() * i)
        if number >= sys.maxsize:
            number = 0
        else:
            number = number + 1
        #print(number)



def run(options):
    if "crash" in options:
        takeoff(options, crash=True)
    if "maxTemp" in options:
        takeoff(options)

#Starts up the all engines
#Will continuously monitor their temperature and pass on this information
#if specified not to crash
def takeoff(options, crash=False):
    global targetTemp
    if "maxTemp" in options:
        targetTemp = options["maxTemp"]
    elif crash: #Be careful!!!
        targetTemp = 1000 #will crash long before it reaches this :)

    nprocs = cpu_count()
    with Pool(nprocs) as pool:
        pool.imap(rev_the_engines, range(nprocs))
        while True:
            if not crash:
                currentTemp.value = get_CPU_tempurate()
            sleep(1)