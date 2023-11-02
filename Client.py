# Client Script
import socket
from random import*

HEADER=256
FORMAT='utf-8'
PORT=8081
SERVERIP="127.0.0.1"#socket.gethostbyname(socket.gethostname())
ADDR=(SERVERIP,PORT)
timestep=1

def receive(client):
    msg_length=client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length=int(msg_length)
        msg=client.recv(msg_length).decode(FORMAT)
    return msg

def send(client,msg):
    message=str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(ADDR)
    # prisoner_port = client.getsockname()[1]
    salu=receive(client)
    print(salu)

    flag=0
    while True:
        try :
            L = int(receive(client))
            R = int(receive(client))
            print("Range received = [", L,",", R,"]", sep="")
            break
        except: print("Range not received")

    while True:
        #Printing timestep
        print("Timestep",timestep)
        timestep+=1
        #Checking for any new escaped prisoners
        while True:
            escaped_prisoner=receive(client)
            if escaped_prisoner=="no more escaped prisoners":
                break
            else:
                print(escaped_prisoner)
        
        msg=receive(client)
        if msg=="Start":
            # Generate a random number Y within the current search range
            Y=randint(L, R)
            print("My guess is", Y)
            # Send the guess Y to the server
            send(client,str(Y))

            # Receive the server's response
            #try: 
            response = receive(client)
            #except: print("No response received")
            print(response, "\n")
            # Updating range based on server's response
            if response=='[SERVER] HIGH':
                R=Y-1
            elif response=='[SERVER] LOW':
                L=Y+1
            elif response=='[SERVER] CORRECT':
                flag=1

        # Check if the client has escaped and print the escape message
        if flag:
            print("You have escaped. Terminating program...")
            break