#CSNETWK: Message Board Project – Client
#S12

#CHUA, Jeric Kerby G.
#MADERAZO, Rafael Nicholas E.
#PASTORAL, Eugenio II G.

#CAGAOAN, John Henry F.
#FAVOR, Caila Joice C.
#SALAZAR, Jacob Israel R.


import socket
import sys
import json
import subprocess
import platform

""" This function clears the console. """
def clear():
    command = "cls" if platform.system().lower()=="windows" else "clear"
    return subprocess.call(command, shell = True)

""" This function sends a registration request to the server. """
def register():
    while True:
        clear()
        global username
        username = input('Enter preferred username: ')
        print('Registering "%s".' % username)
        u = json.dumps({"command":"register", "username":username})
        sent = sock.sendto(bytes(u,"utf-8"), (server_host, dest_port))

        data, server = sock.recvfrom(1024)
        response = json.loads(data)

        if response["code_no"] == 401:
            print('Registered successfully.')
            break
            input("Press enter to continue...")
        elif response["code_no"] == 502:
            print('%s is already registered. Try a different username.' % username)
            input("Press enter to continue...")
        else:
            print('%s cannot be registered. Try again.')
            input("Press enter to continue...")

""" This function handles message board requests. """
def messageboard():
    global username
    sock.settimeout(None)
    while True:
        message = input('Enter message: ')
        m = json.dumps({"command":"msg", "username":username, "message":message})
        sent = sock.sendto(bytes(m,"utf-8"), (server_host,dest_port))

        data, server = sock.recvfrom(1024)
        response = json.loads(data)

        if response["code_no"] == 401 and message != "logout":
            print('Message sent successfully.')
        elif response["code_no"] == 501 and message != "logout":
            print('%s is not registered. Register to join the message board.' % username)
            input("Press enter to continue...")
            break
        elif response["code_no"] == 401 and message == "logout":
            print('Disconnecting...')
            exit()
        else:
            print('Message cannot be sent. Try again.')
            input("Press enter to continue...")

""" This function sends a deregistration request to the server. """
def deregister():
    print('Disconnecting...')
    m = json.dumps({"command":"deregister", "username":username})
    sent = sock.sendto(bytes(m,"utf-8"), (server_host,dest_port))

    data, server = sock.recvfrom(1024)
    response = json.loads(data)

    if response["code_no"] == 401:
        print('You have been disconnected.')
        input("Press enter to continue...")
    elif response["code_no"] == 501:
        print('%s is not registered. Register to join the message board.' % username)
        input("Press enter to continue...")
    else:
        print('Deregistering was unsuccessful. Try again.')
        input("Press enter to continue...")
        exit()

""" This function displays the menu. """
def menu():
    registered = False
    while True:
        clear()
        if registered == True:
            selection = input("""1: Register\n2: Message board\n3: Exit\n\nPlease enter your choice: """)
            if selection =='1':
                register()
            elif selection == '2':
                messageboard()
            elif selection == '3':
                print('Closing socket.')
                sock.close()
                exit()
            else:
                print("Unknown option selected. Try again.")
                input("Press enter to continue...")
        else:
            selection = input("""1: Register\n2: Exit\n\nPlease enter your choice: """)
            registered = True
            if selection =='1':
                register()
            elif selection == '2':
                print('Closing socket.')
                sock.close()
                exit()
            else:
                print("Unknown option selected. Try again.")
                input("Press enter to continue...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    clear()
    try:
        server_host = input('Enter IP address of message board server: ')
        dest_port = int(input('Enter port of message board server: '))
        sent = sock.sendto(bytes(json.dumps({"command":"connect"}),"utf-8"), (server_host, dest_port))
        sock.settimeout(3.0)
        if sock.recvfrom(1024):
            input("Connection established. Press enter to continue...")
        username = ""

        while True:
            menu()
    except socket.timeout as e:
        print('Connection not established. Try again.')
        input("Press enter to continue...")
        clear()

        continue
    finally:
        sock.close()
