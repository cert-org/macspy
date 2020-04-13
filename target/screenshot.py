import datetime
import textwrap
import sys
import time

from send_to_server import add_to_send_queue
from global_variables import run_command, programDirectory
from launch_agent_factory import create_launch_agent

def capture_screenshot():
    #Generate name for screenshot file based on current date and time
    currentDate = datetime.date.today().strftime("%b-%d-%Y")
    currentTime = datetime.datetime.now().strftime("%H-%M-%S")
    screenshotFilename = "./Data/screenshot/" + "Screenshot_" + currentDate + "_" + currentTime + ".png"

    #Take screenshot
    run_command("screencapture -x " + screenshotFilename)

    #Send to server
    add_to_send_queue(screenshotFilename)


def run(options):
    if "startTime" not in options:
        capture_screenshot()
    else:
        global programDirectory
        options["workingDirectory"] = programDirectory
        options["programFile"] = programDirectory + "/screenshot.py"
        options["programArguments"] = []
        options["programArguments"].append(options["frequency"]["seconds"])

        create_launch_agent(options)


#called by launch agent
#started at first capture
def main():
    secondsBetweenCaptures = int(sys.argv[1])
    if secondsBetweenCaptures == 0:
        secondsBetweenCaptures = 60
    counter = 0
    while counter < 60:
        capture_screenshot()
        counter += secondsBetweenCaptures
        if counter < 60:
            time.sleep(secondsBetweenCaptures)
    
        
if __name__ == '__main__':
    main()