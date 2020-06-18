import nltk
from textblob import TextBlob as blob
import speech_recognition as sr
import sentiment_mod as s

import argparse
import random
import time

from pythonosc import udp_client

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=12000,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)


##create an object from the text blob
##text blob contains information about Part of Speech tagging
tb = blob('Hi, here is my sentiment analysis of speech!')

##object of the speech recognition
r = sr.Recognizer()

iter_num = 10
index = 0
##the loop below is running 10 times
while(index<iter_num):
  with sr.Microphone() as source:
    print('Say Something')
    ##if there is no sound for 5 seconds, it will stop recording and move on
    ##to the next speech message
    audio = r.listen(source, timeout=5)

    try:
            text = r.recognize_google(audio)
            tb = blob(text)
            sentiment_value, confidence = s.sentiment(text)
            print(tb, sentiment_value, confidence)
            sendstring = confidence
            client.send_message('/address', str(sentiment_value))

    except:
            print('Sorry... try again')
            index = index + 1


