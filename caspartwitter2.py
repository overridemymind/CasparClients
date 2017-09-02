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
templateSelect = ""

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

def casparStart(xmldata):
	cgCommand = ('CG 1-999 ADD 1 ' + templateSelect + ' 0 "<templateData>' 
		+ xmldata + '</templateData>"\r\n')
	cgCommand = cgCommand.encode('utf-8')
	caspar.send(cgCommand)
	print ((caspar.recv(1024)).decode('utf-8'))
	sleep(2)
	cgCommand = ('CG 1-999 PLAY 1\r\n')
	cgCommand = cgCommand.encode('utf-8')
	caspar.send(cgCommand)

def casparStop():
	cgCommand = ('CG 1-999 STOP 1\r\n')
	cgCommand = cgCommand.encode('utf-8')
	caspar.send(cgCommand)
	print ((caspar.recv(1024)).decode('utf-8'))

def formatTweet(username, tweet):
	nameXML = ('<componentData id=\\"f0\\"><data id=\\"text\\" value=\\"' 
		+ username + '\\"/></componentData>')
	if len(tweet) > 80:
		text = tweet.split()
		iterate = 0
		firstLine = []
		secondLine = []
		for t in text:
			if iterate < 10:
				firstLine.append(t)
				iterate = iterate + 1
			elif iterate >= 10:
				secondLine.append(t)
				iterate = iterate + 1
		tweetL1 = ' '.join(firstLine)
		tweetL2 = ' '.join(secondLine)
		tweetXMLa = ('<componentData id=\\"f1\\"><data id=\\"text\\" value=\\"' 
			+ tweetL1 + '\\"/></componentData>')
		tweetXMLb = ('<componentData id=\\"f2\\"><data id=\\"text\\" value=\\"' 
			+ tweetL2 + '\\"/></componentData>')
		tweetXML = tweetXMLa + tweetXMLb
	else:
  		tweetXML = ('<componentData id=\\"f1\\"><data id=\\"text\\" value=\\"' 
			+ tweet + '\\"/></componentData>')
	xmlToSend = nameXML + tweetXML
	casparStart(xmlToSend)
	sleep(10)
	casparStop()

while True:
	public_tweets = api.search('', lang='en')
	for tweets in public_tweets:
		handle = '@' + tweets.user.screen_name
		tweetText = tweets.text
		formatTweet(handle, tweetText)
	sleep(5)
