import datetime
from global_variables import run_command
from send_to_server import add_to_send_queue
"""
Finds out when user has been active on their computer over the last week
"""
def run(options):
    #Generate name for screenshot file based on current date and time
    moduleDirectory = "./Data/usage_intervals/"
    currentDate = datetime.date.today().strftime("%b-%d-%Y")
    currentTime = datetime.datetime.now().strftime("%H-%M-%S")
    usageIntervalsFilename = moduleDirectory + "UsageIntervals" + currentDate + "_" + currentTime + ".txt"
    
    #get usage intervals and send to server
    run_command(f"""pmset -g log | egrep 'Wake from|Entering Sleep' | cut -f1 | cut -d" " -f1,2,4 > {usageIntervalsFilename}""")
    add_to_send_queue(usageIntervalsFilename)