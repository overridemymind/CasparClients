import socket, sys
from datetime import datetime
from time import sleep
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

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
  print("Connected to caspar")
except socket.error:
  print("Failed to connect to CasparCG. Check the correct ip and port have been input")
  exit(0)

def sendTweet(username, tweet):
  templateSelect = ""
  nameXML = ('<componentData id=\\"f0\\"><data id=\\"text\\" value=\\"' 
   	+ username + '\\"/></componentData>')
  tweetXML = ('<componentData id=\\"f2\\"><data id=\\"text\\" value=\\"' 
   	+ tweet + '\\"/></componentData>')
  cgCommand = ('CG 1-999 ADD 1 ' + templateSelect + ' 0 "<templateData>' 
   	+ nameXML + tweetXML + '</templateData>"\r\n')
  cgCommand = cgCommand.encode('utf-8')
  caspar.send(cgCommand)
  print ((caspar.recv(1024)).decode('utf-8'))
  sleep(2)
  cgCommand = ('CG 1-999 PLAY 1\r\n')
  cgCommand = cgCommand.encode('utf-8')
  caspar.send(cgCommand)
  print ((caspar.recv(1024)).decode('utf-8'))
  sleep(10)
  cgCommand = ('CG 1-999 STOP 1\r\n')
  cgCommand = cgCommand.encode('utf-8')
  caspar.send(cgCommand)
  print ((caspar.recv(1024)).decode('utf-8'))
  sleep(3)

while True:
	public_tweets = api.search('', lang='en')
	for tweets in public_tweets:
		handle = '@' + tweets.user.screen_name
		tweetText = tweets.text
		sendTweet(handle, tweetText)
	sleep(5)
