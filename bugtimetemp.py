import socket, sys
from datetime import datetime
import pyowm

# OpenWeatherMap API Key goes here
owmAPIkey = ''
owmLocation = ''
owmTempFormat = 'fahrenheit'
casparServer = ''
casparPort = 5250

caspar = None

def exit(i):
  global caspar
  if not caspar == None:
    caspar.close
  sys.exit(i)

try:
  print("System running...")
  caspar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  caspar.connect((casparServer, casparPort))
  owm = pyowm.OWM(owmAPIkey)
  print("Connected to caspar")
except socket.error:
  print("Failed to connect to CasparCG. Check the correct ip and port have been input")
  exit(0)

holdTime = ""
holdTemp = ""

def funcGetTemp():
  observation = owm.weather_at_place(owmLocation)
  currentObs = observation.get_weather()
  obsTemp = currentObs.get_temperature(owmTempFormat)
  obsTemp = int(obsTemp["temp"])
  return obsTemp

def sendTimeTemp(currentTime, currentTemp):
  templateSelect = "HDTV"
  timeXML = ('<componentData id=\\"f0\\"><data id=\\"text\\" value=\\"' 
    + currentTime + '\\"/></componentData>')
  tempXML = ('<componentData id=\\"f1\\"><data id=\\"text\\" value=\\"' 
    + currentTemp + '°F\\"/></componentData>')
  cgCommand = ('CG 1-1000 ADD 1 ' + templateSelect + ' 1 "<templateData>' 
    + timeXML + tempXML + '</templateData>"\r\n')
  cgCommand = cgCommand.encode('utf-8')
  caspar.send(cgCommand)
  print ((caspar.recv(1024)).decode('utf-8'))

while True:
  getTime = datetime.now().strftime('%-I:%M %p')
  if holdTemp == "":
    interval = 5
  else:
    interval = int(datetime.now().strftime('%M'))
  if getTime != holdTime:
    if interval % 5 == 0:
      getTemp = funcGetTemp()
      holdTemp = getTemp
    holdTime = getTime
    sendTimeTemp(holdTime, str(holdTemp))

exit(1)
