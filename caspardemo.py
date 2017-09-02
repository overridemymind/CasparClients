import socket, sys

caspar = None

def exit(i):
  global caspar
  if not caspar == None:
    caspar.close
  sys.exit(i)

try:
  print("System running...")
  caspar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  caspar.connect(("YOUR_IP_HERE", 5250))
  print("Connected to caspar")
except socket.error:
  print("Failed to connect to CasparCG. Check the correct ip and port have been input")
  exit(0)

while True:
  try:
    #command = raw_input("Enter command: ")
    command = input("Enter command: ")
    command = command + "\r\n"
    command = command.encode('utf-8')
    #caspar.send(command + "\r\n")
    caspar.send(command)
    print ((caspar.recv(1024)).decode('utf-8'))
  except socket.error:
    print("System error - command failed.")
    exit(1)
