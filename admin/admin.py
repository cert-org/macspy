# server.py

import socket                   
import threading
import time
from command_processor import create_message
import json

port = 7584                   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = "127.0.0.1"  
s.bind((host, port))            
s.listen(1)                     
print('Server listening....')

conn, addr = s.accept()     
print(addr)

#Waits to receive files from client and unpacks them 
def receiveDataFromConnnection():
    while True:
        data = conn.recv(4096).decode()
        filename, filesize = data.split("<sep>")
        filesize = int(filesize)
        with open(filename, "wb") as newFile:
            while filesize > 0:
                data = conn.recv(4096)

                if not data:
                    break

                newFile.write(data)
                filesize -= 4096
        

def main():
    dataReceiveThread = threading.Thread(target = receiveDataFromConnnection)
    dataReceiveThread.start()
    
    #Send commands to client
    while True:
        command = input("Enter a command: ")
        options = create_message(command)
        if options != None:
            print("Request sent!")
            conn.sendall(str.encode(json.dumps(options)))

main()

