#CSNETWK: Message Board Project – Server
#S12

#CHUA, Jeric Kerby G.
#MADERAZO, Rafael Nicholas E.
#PASTORAL, Eugenio II G.

#CAGAOAN, John Henry F.
#FAVOR, Caila Joice C.
#SALAZAR, Jacob Israel R.

import socket
import json

UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 5015
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
database = []
clients = []
print("starting up on %s:%s" % (UDP_IP,UDP_PORT))

""" This function displays the current usernames and clients connected. """
def display():
    print("users on board: ")
    print(database)
    print("clients: ")
    print(clients)

""" This function checks if the client's username is present in the list. """
def checkUsername(username):
    if username in database:
        return True
    return False

""" This function checks if the client has been logged and connected. """
def checkClient(address):
    if address in clients:
        return False
    else:
        clients.append(address)
        return True

""" This function registers a client. """
def register(data,addr):
    response = json.loads(data)
    if checkUsername(response["username"]):
        commands(502, addr)
    else:
        database.append(response["username"])
        display()
        commands(401, addr)

""" This function evaluates whether a request is valid or not. """
def commands(codenumber, address):
    if codenumber == 401:
        u = json.dumps({"command": "ret_code", "code_no": 401})
        sock.sendto(bytes(u, "utf-8"), address)
    elif codenumber == 502:
        u = json.dumps({"command": "ret_code", "code_no": 502})
        sock.sendto(bytes(u, "utf-8"), address)


""" This function connects the client to the server. """
def connect_client(address):
    if checkClient(address):
        sock.sendto(bytes(json.dumps({"command": "connect"}), "utf-8"), address)

""" This function deregisters the client. """
def deregister(data,addr):
    removed = False
    response = json.loads(data)
    username = response["username"]
    print("user " + username + " exiting....")
    commands(401,addr)
    database.remove(username)
    display()

""" This function handles message sending. It sends the message
    to the server. """
def message(data,addr):
    response = json.loads(data)
    u_temp = response["username"]
    print(checkUsername(u_temp))
    if checkUsername(u_temp):
        if response["message"] != "logout":
            commands(401, addr)
            print(response["username"] +":"+ " " + response["message"])
        else:
            commands(401, addr)
            deregister(data,addr)
    else:
        commands(501, addr)

""" This function initiates the server processes. """
def Listen():
    while True:
        data, addr = sock.recvfrom(1024)
        response = json.loads(data)
        if response["command"] == "connect":
            connect_client(addr)
        elif response["command"] == "register":
            register(data,addr)
        elif response["command"] == "msg":
            message(data,addr)
        elif response["command"] == "deregister":
            deregister(data,addr)

Listen()
print("end of program")
sock.close()
