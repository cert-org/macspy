# Welcome. This is the department in charge sending data to the server
import subprocess
import os
import threading
import time

import global_variables

sendQueueLock = threading.Lock()

def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err

def add_to_send_queue(filename):
    global sendQueueLock
    sendQueueLock.acquire(True)
    with open("sendQueue.txt", "a") as sendQueue:
        sendQueue.write(filename + "\n")
    sendQueueLock.release()

def send_data():
    global sendQueueLock

    while True:
        # wait until connection to server is open
        if global_variables.isConnectedToServer == False:
            time.sleep(1)
            continue

        sendQueueLock.acquire(True)

        firstFilepath = None
        # Get first file in queue to be sent to server
        with open("sendQueue.txt", "r+") as sendQueue:
            firstFilepath = sendQueue.readline()
            # Remove this file from the queue
            if firstFilepath:
                firstFilepath = firstFilepath[:-1]
                nextLines = sendQueue.read()
                sendQueue.seek(0)
                sendQueue.write(nextLines)
                sendQueue.truncate()

        sendQueueLock.release()

        if firstFilepath:
            # convert file to zip file
            zipFilename = os.path.basename(firstFilepath) + ".zip"
            run_command("zip -r -j -X " + zipFilename + " " + firstFilepath)
            # send file name and size to server
            filesize = os.path.getsize(zipFilename)
            global_variables.serverSocket.sendall(f"{zipFilename}<sep>{filesize}".encode())

            # send zip file to server
            with open(zipFilename, "rb") as zipfile:
                global_variables.serverSocket.sendfile(zipfile)

            #remove files sent
            run_command("rm " + zipFilename)
            run_command("rm " + firstFilepath)


        else:
            time.sleep(1)
        
