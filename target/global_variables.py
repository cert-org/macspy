import socket
import os
import subprocess


def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err

global serverSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global isConnectedToServer
isConnectedToServer = False
global pythonInterpreter
pythonInterpreter = str(run_command("which python3").decode("utf-8"))[:-1]
global programDirectory
programDirectory = os.path.expanduser("~/Library/macspy")
