import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.on('userdc')
def userDc(data):
    print("user has disconnected: ", data)


@sio.on('usercon')
def userCon(data):
    print("user has connect: ", data)


# when server broadcasts a message, this event will catch it and print it
@sio.on('broadcast')
def serverMessage(data):
    if (data['user'] != userName):
        print(f"{data['user']}: {data['message']}")


# setting up user environment, sets up the users username and attempts to connect to the socket
chat = False
userName = input("please input username: ")
try:
    print("type exit at any time to disconnect\nattempting to connect...")
    sio.connect('http://localhost:3000')
    # set user name to be the string entered by the user, and append a # followed by the first 5 digits of the sid
    userName = userName + "#" + sio.sid[0:5]
    chat = True
except:
    print("Could not connect to server")


# main loop that will allow user to keep entering messages until they type exit. Typing exit will
# disconnect the user and end the loop, which also ends the program
while (chat):

    userInput = input("")
    if (userInput == 'exit'):
        print("disconnecting...")
        sio.disconnect()
        chat = False
    else:
        sio.emit('message', {'user': userName, 'message': userInput})
