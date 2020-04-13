from global_variables import run_command, pythonInterpreter, programDirectory
import random
import string
import os, sys
import datetime, time
from dateutil import parser

"""
Automates the process of generating launch agent .plist files
These can be very long and repetitive if the data is collected at frequent intervals
Used for setting up custom intervals for data collecion. Like a cron job, but this is not
supported on newer versions of OSX. Launchd can do the same things though.
"""

def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def is_time_greater(start, end):
    if start["hour"] > end["hour"] or (start["hour"] == end["hour"] and start["minute"] > end["minute"]):
        print("start time is greater than end time")
        return True
    return False

def create_launch_agent(options):
    global pythonInterpreter
    timeNow = datetime.datetime.now()

    if timeNow.weekday() > options["weekday"]:
        offset = (6 - timeNow.weekday()) + options["weekday"]
    elif timeNow.weekday() == options["weekday"]:
        now = {}
        now["hour"] = timeNow.hour
        now["minute"] = timeNow.minute
        if is_time_greater(now, options['startTime']):
            offset = 7
        else:
            offset = 0
    else:
        offset = options["weekday"]

    print("offset="+str(offset))
    timeNow += datetime.timedelta(days=offset)
    expiryDate = timeNow.replace(hour=options['endTime']['hour'], minute=options['endTime']['minute'], second=0)

    #store expiry time
    launchAgentName = "macspy"+options["module"]+randomString()+"_"+str(expiryDate)+"_"

    launchAgentConfig = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.macspy_{launchAgentName}.app</string>
        <key>WorkingDirectory</key>
        <string>{options["workingDirectory"]}</string>
        <key>ProgramArguments</key>
        <array>
            <string>{pythonInterpreter}</string>
            <string>{options["programFile"]}</string>
"""
    for argument in options["programArguments"]:
        launchAgentConfig += f"""\
            <string>{argument}</string>
"""
    launchAgentConfig += """\
        </array>
"""

    launchAgentConfig += """\
        <key>StartCalendarInterval</key>
        <array>
"""
    #hours/minutes always exist, sometimes zero
    weekday = (options["weekday"] + 1) % 7
    hour = options["startTime"]["hour"]
    minute = options["startTime"]["minute"]
    if "frequency" in options:
        frequencyHours = options["frequency"]["hours"]
        frequencyMinutes = options["frequency"]["minutes"]
        if frequencyMinutes == 0:
            frequencyMinutes = 1

        while hour < options["endTime"]["hour"] or minute < options["endTime"]["minute"]:
            launchAgentConfig += f"""\
            <dict>
                <key>Hour</key>
                <integer>{hour}</integer>
                <key>Minute</key>
                <integer>{minute}</integer>
                <key>Weekday</key>
                <integer>{weekday}</integer>
            </dict>
"""
            hour += frequencyHours
            minute += frequencyMinutes
            if minute >= 60:
                hour += 1
                minute %= 60
    else: #one off job
        launchAgentConfig += f"""\
            <dict>
                <key>Hour</key>
                <integer>{hour}</integer>
                <key>Minute</key>
                <integer>{minute}</integer>
                <key>Weekday</key>
                <integer>{weekday}</integer>
            </dict>
"""

    launchAgentConfig += """\
        </array>
"""

    launchAgentConfig += """\
    </dict>
</plist>
"""
    #create file
    launchAgentFile = os.path.expanduser("~/Library/LaunchAgents") + "/" + launchAgentName + ".plist"
    print(launchAgentFile)
    with open(launchAgentFile, "w") as newLaunchAgentFile:
        newLaunchAgentFile.write(launchAgentConfig)

    #load launch agent
    run_command("launchctl load " + "\"" + launchAgentFile + "\"")



#Every hour, go though and delete expired launch agents
def delete_expired_launch_agents():
    launchAgentDirectory = os.path.expanduser("~/Library/LaunchAgents")
    while True:
        timeNow = datetime.datetime.now()
        for launchAgent in os.listdir(launchAgentDirectory):
            if "macspy" in launchAgent and launchAgent[-7:-6] == "_":
                print(launchAgent)
                #get datetime object which is part of filename
                expiryDate = parser.parse(launchAgent.split("_")[1])
                print("exp="+str(expiryDate))
                print("now="+str(timeNow))
                if expiryDate < timeNow:
                    time.sleep(3)
                    run_command("rm -f " + launchAgentDirectory + "/" + "\""+launchAgent+"\"")

        time.sleep(3600)