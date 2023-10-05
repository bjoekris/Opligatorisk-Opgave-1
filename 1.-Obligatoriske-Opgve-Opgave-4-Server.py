from socket import *
import threading
import random
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


def HandleClient(connectionSocket, address):
 connectionSocket.send('Type "Random" or "Calculator" to get the corresponding function.'.encode())
 sentence = connectionSocket.recv(1024).decode().lower()
 txtRecieved = 'From client {addr}: ', sentence
 txtString = str(txtRecieved)
 txtStart = txtString.format(addr = addr)
 print(txtStart)
 connectionSocket.send(' '.encode())

 if 'random' in sentence:
  handleRandom(connectionSocket, addr)
 
 elif 'calculator' in sentence:
  handleCalculator(connectionSocket, addr)

 else:
  handleWrongCommand(connectionSocket, addr)


def handleWrongCommand(connectionSocket, address):
 connectionSocket.send('Wrong command, did you input a valid command word?'.encode())
 handleClose(connectionSocket, addr)
 print('Wrong command from client: ', addr)
 print('Connection closed for client: ', addr)
 connectionSocket.close()


def handleClose(connectionSocket, address):
 connectionSocket.send(' Connection ended'.encode())


def handleRandom(connectionSocket, address):
 connectionSocket.send('Type two numbers, the server will respond with a random number between them.'.encode())
 sentence = connectionSocket.recv(1024).decode()
 txtRecieved = 'From client {addr}: ', sentence
 txtString = str(txtRecieved)
 txtStart = txtString.format(addr = addr)
 print(txtStart)
 
 num1 = int(sentence.split(' ')[0])
 num2 = int(sentence.split(' ')[1])
 num = random.randrange(num1,num2)
 numStr = f'Your random number between {num1} and {num2} is: {num}'
 print(f'Client random number is: {num}')
 
 connectionSocket.send(numStr.encode())
 handleClose(connectionSocket, addr)
 print('Connection closed for client: ', addr)
 connectionSocket.close()


def handleCalculator(connectionSocket, address):
 connectionSocket.send('Type "Add", "Subtract", "Multiply", or "Divide" to get the corresponding function. Type two numbers after the command word, the server will use them for the calculation.'.encode())
 sentence = connectionSocket.recv(1024).decode()
 txtRecieved = 'From client {addr}: ', sentence
 txtString = str(txtRecieved)
 txtStart = txtString.format(addr = addr)
 print(txtStart)

 a = int(sentence.split(' ')[1])
 b = int(sentence.split(' ')[2])

 txt = 'The {calc} of {num1} {x} {num2} = {result}'
 txtCalc = ''
 
 if 'add' in sentence:
  y = a + b
  txtCalc = txt.format(calc = 'addition', num1 = a, x = '+', num2 = b, result = y)
  print(txtCalc)
 
 elif 'subtract' in sentence:
  y = a - b
  txtCalc = txt.format(calc = 'subtraction', num1 = a, x = '-', num2 = b, result = y)
  print(txtCalc)
  
 elif 'multiply' in sentence:
  y = a * b
  txtCalc = txt.format(calc = 'multiplication', num1 = a, x = '*', num2 = b, result = y)
  print(txtCalc)
  
 elif 'divide' in sentence:
  y = a / b
  txtCalc = txt.format(calc = 'divition', num1 = a, x = '/', num2 = b, result = y)
  print(txtCalc)
  
 connectionSocket.send(txtCalc.encode())
 handleClose(connectionSocket, addr)
 print('Connection closed for client: ', addr)
 connectionSocket.close()
 

print('The server is ready to receive')
while True:
 connectionSocket, addr = serverSocket.accept()
 print('Connection from client, address:',addr)
 threading.Thread(target=HandleClient,args=(connectionSocket,addr)).start()