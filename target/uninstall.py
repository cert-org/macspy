import os
import subprocess

def run_command(command):
    """Runs a system command and returns its response."""
    out, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    return out + err

def run(options):
    #Where program and its resources live
    programDirectory = os.path.expanduser("~/Library/macspy")

    #Delete all macspy launch agents
    lauchAgentDirectory = os.path.expanduser("~/Library/LaunchAgents")
    for filename in os.listdir(lauchAgentDirectory):
        if "macspy" in filename:
            run_command("launchctl unload " + filename)
            run_command("rm -f " + lauchAgentDirectory + "/" + filename)

    #Delete program directory
    run_command("rm -rf " + programDirectory)
    

if __name__ == '__main__':
    options = {}
    run(options)