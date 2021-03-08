#----------------------------------------------------------------
## Name: Taariq McDonald
## Student Number: 215465214
## Course: EECS 3214
## Assignment 1: Question #3
#----------------------------------------------------------------
import socket
import ssl
import base64


serverName = "smtp.gmail.com" 
serverPort = 587 

def getReceiver():
    recUser = input("Please enter the receivers email: ")
    print('\n')
    return recUser

def getMessage():
    clientMes = input("Please enter the message that you would like to send: ")
    print('\n')
    return clientMes

def startEmail(receiver, text):
    #-------------------------- Create a Client Socket---------------------------------
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create an INET, STREAMing socket
    clientSocket.connect((serverName, serverPort)) #connects to server
    #----------------------------------------------------------------------------------

    #-------------------------- 3 Way Handshake----------------------------------------
    data = clientSocket.recv(4096) #gets the data that the server has sent back to the client
    print("Client: Initiate 3 way handshake with mail server")
    print('Server Response: ', data.decode())
    #-------------------3 Way Handshake done. TCP connection is established------------

    #------------------------- Sending the HELO command -------------------------------
    hCommand = 'HELO smtp.gmail.com\r\n'
    clientSocket.send(hCommand.encode('utf-8')) #the message needs to be in bytes. encode('utf-8') converts it bytes
    data2 = clientSocket.recv(4096)
    client = hCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data2.decode())
    #------------------------- HELO command successfully sent -------------------------

    #---------------------- Request verification of the user --------------------------
    vCommand = 'VRFY ' + receiver + '\r\n' #########################had taariqmcdonald here instead of receiver previously
    clientSocket.send(vCommand.encode('utf-8'))
    data3 = clientSocket.recv(4096)
    client = vCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data3.decode())
    #---------------------- Request Verification Completed ----------------------------

    #---------------------- Issue a STARTTLS command ----------------------------------
    #This tells an email server that an email client wants to turn an existing insecure connection into a secure connection
    sCommand = 'STARTTLS\r\n'
    clientSocket.send(sCommand.encode('utf-8'))
    data4 = clientSocket.recv(4096)
    client = sCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data4.decode())
    #---------------------- Issuing of STARTTLS command successful --------------------

    #---------------------- Client does TLS handshake ---------------------------------
    tlsClientSock = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLSv1)
    #---------------------- Successful TLS handshake ----------------------------------

    #---------------------- Authentication --------------------------------------------
    user = ("\x00addamsjosh274@gmail.com\x003214_testdum").encode()
    user_encode = base64.b64encode(user)
    aCommand = 'AUTH PLAIN '.encode() + user_encode + '\r\n'.encode()
    tlsClientSock.send(aCommand)
    data5 = tlsClientSock.recv(4096)
    print("Client: Authenticate this email server")
    print('Server Response: ', data5.decode())
    #---------------------- Authentication Successful ---------------------------------

    #---------------------- Send the MAIL FROM command --------------------------------
    #Indicates who is sending the email
    mCommand = 'MAIL FROM: <addamsjosh274@gmail.com>\r\n'
    tlsClientSock.send(mCommand.encode('utf-8'))
    data6 = tlsClientSock.recv(4096)
    client = mCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data6.decode())
    #--------------------- MAIL FROM command sent successfully ------------------------

    #------------------------ Send the RCPT TO command --------------------------------
    #Indicates who is receiving the email
    rCommand = 'RCPT TO: <' + receiver + '>\r\n' #########removed the tmmstar99@gmail.com
    tlsClientSock.send(rCommand.encode('utf-8'))
    data7 = tlsClientSock.recv(4096)
    client = rCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data7.decode())
    #--------------------- RCPT TO command sent successfully --------------------------

    #-------------------------- Send the DATA command ---------------------------------
    #Indicates that you are about to send the text of the message
    dCommand = 'DATA\r\n'
    tlsClientSock.send(dCommand.encode('utf-8'))
    data8 = tlsClientSock.recv(4096)
    client = dCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data8.decode())
    #-------------------------- DATA command successfully sent ------------------------

    #-------------------------- Send the body of Email --------------------------------
    message = ''+ text + '\r\n.\r\n'    #'Hello, I hope this email finds you well\r\n.\r\n'
    tlsClientSock.send(message.encode('utf-8'))
    data9 = tlsClientSock.recv(4096)
    client = message.split('\r\n.\r\n')
    print('Client Message: ', client[0])
    print('Server Response: ', data9.decode())
    #-------------------------- Email Successfully sent -------------------------------

    #-------------------------- Send the QUIT command ---------------------------------
    #Indicates that the conversation is over
    qCommand = 'QUIT\r\n'
    tlsClientSock.send(qCommand.encode('utf-8'))
    data10 = tlsClientSock.recv(4096)
    client = qCommand.split('\r\n')
    print('Client: ', client[0])
    print('Server Response: ', data10.decode())
    #-------------------------- QUIT command sent successfully ------------------------

    clientSocket.close() #close the clients socket

def main():
    input = getReceiver()
    input2 = getMessage()
    startEmail(input, input2)

if __name__ == '__main__':
    main()
