# Server Script
# Importing all the modules required
import socket
from random import*

HEADER=256
FORMAT='utf-8'
PORT=8081
SERVERIP="127.0.0.1"#socket.gethostbyname(socket.gethostname())
ADDR=(SERVERIP,PORT)

prisoner_escape=[] #list containing the aliases of all the prisoners that escape
temp_list=[]
L=randint( 1, 400)
R=randint( L+10000, L+100000)
X=randint( L, R)
prisoner_list=[] #list containing the socket objects of all the prisoners

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

#Function to handle each client connection
def client_communication(prisoner_list):
    global prisoner_escape
    global temp_list
    while True:
        #Sending names of the prisoners as and when they escape to the individual terminals
        if temp_list!=prisoner_escape:
            for j in prisoner_escape:
                if j not in temp_list:
                    for i in range(4):
                        if(i+1) not in prisoner_escape:
                            client_socket=prisoner_list[i]
                            send(client_socket,"\n[SERVER]!!!!  PRISONER "+str(j)+" HAS ESCAPED  !!!!\n")
                    temp_list.append(j)
        for i in range(4):
            if(i+1) not in prisoner_escape:
                client_socket=prisoner_list[i]
                send(client_socket,"no more escaped prisoners")

        #Processing the guesswork     
        for i in range(4):
            if(i+1) not in prisoner_escape:
                client_socket=prisoner_list[i]

                send(client_socket,"Start")
                # Receiving a guess from the prisoner
                guess=int(receive(client_socket))
                
                if guess>X:
                    send(client_socket,'[SERVER] HIGH')
                elif guess<X:
                    send(client_socket,'[SERVER] LOW')       
                elif guess==X:
                    send(client_socket,'[SERVER] CORRECT')
                    prisoner_escape.append(i+1)

        if(len(prisoner_escape)==4):
            break

#--------------------------------END OF THE CLIENT FUNCTION-----------------------------

# MAIN

with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)

    #Listening for incoming connection requests
    server_socket.listen(4)
    print("Initial range is ", L,"to", R, "and the lucky number is=", X)
    print("Waiting for connection...")

    conn=True
    while conn:
        client_socket, client_address = server_socket.accept()
        # Add to the prisoner port list
        prisoner_list.append(client_socket)
        print("New connection @ ", client_address)

        #Salutation
        msg="Welcome to the Server, successfully connected!"
        send(client_socket,msg)

        # Sending initial range values
        send(client_socket,str(L))
        send(client_socket,str(R))

        if len(prisoner_list) == 4:
            conn=False
    client_communication(prisoner_list)

print("\nOrder of escape :")
for i in prisoner_escape:
    print("Prisoner number "+str(i))