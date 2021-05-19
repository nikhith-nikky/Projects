# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 18:12:10 2020

@author: Nikhith
"""
# Authors: Nikhith Theddu
# This program creates a chat bot assistant ELIZA, a psychotherapist
# It is an interactive chat bot assistant which constantly takes inputs
# from the user and replies to the user accordingly.
# The functionalities of this chat bot are,
# 1.In the start, the chatbot greets the user by saying good morning or
#   afternoon or evening based on the time of the day.
# 2.To become more interactive the chatbot grabs the name of the user 
#   and displays it for every new message.
# 3.The chatbot also detects the improper language and reports it to
#   the user to use a proper language.
# 4.The chatbot also uses timer and if the user does not enter any input
#   for 20 seconds then the chatbot ask to enter an input.
# 5.If any gibberish is entered the chatbot tells the user that it is
#   not aware of those words.
# 6.If anything other than alphanumeric characters are entered then it
#   asks the user to enter only alphanumeric characters.
# 7.If any question is entered saying 'what is',the chatbot searches for
#   that particular word in the wordnet and gives the meaning of that
#   word.
# 8.The chatbot always has an answer though anything unknown to it is entered
# 9.The program quits on saying quit,bye,exit,good bye.
# The algorithm of the chat bot is, it takes input from the user and 
# and checks for that input in the dictionary of responses which is pre-defined
# if the key is found then a random value from a list of values of the
# corresponding key is taken.
# Additional functionalities: The functionalities 1,3,4,7,8 from the above
# are the additional functionalities.
# Example:
#Good evening, I am ELIZA, your chatbot assistant.
#[Eliza] Hello, Please type in your name
#[user] I am Nikhith

#[Eliza] Hello Nikhith, how are you today?
#[Nikhith] I am good

#[Eliza] Great! How can I help you today?
#[Nikhith] I cannot play

#[Eliza] Do you really cannot play
#[Nikhith] I love my family

#[Eliza] Tell me more about your family.
#[Nikhith] My father is kind

#[Eliza] How do you feel about your father?
#[Nikhith] I am hurt

#[Eliza] Please calm your mind
#[Nikhith] I want to commit suicide

#[Eliza] Why did you feel like commiting?
#[Nikhith] I want to murder

#[Eliza] Why do you have such a feeling?
#[Nikhith] fuck

#[Eliza] Please use a proper language
#[Nikhith] sbdjsbjd

#[Eliza] I am sorry, I am unaware of the word sbdjsbjd
#[Nikhith] what is autism

#[Eliza] (psychiatry) an abnormal absorption with the self; marked by communication disorders and short attention span and inability to treat others as people
#[Nikhith] ?/''

#[Eliza] Please enter a valid input with only alphanumeric characters
#[Nikhith] 
#[Eliza] Are you still there? If yes please enter an input
#yes

#[Eliza] Okay,can you please elaborate a bit?
#[Nikhith] quit

#[Eliza] Good bye. Have a nice day Nikhith.

import re
import nltk
import threading
import nltk
#nltk.download('punkt')
import random
from nltk.corpus import words
#nltk.download('words')
from nltk.corpus import wordnet
#nltk.download('wordnet')
from nltk.tokenize import RegexpTokenizer
import datetime
# creates a dictionary for responses of chat bot
responses = {
             r'(.*)?(\s)?(good|great|fine)':['Great! How can I help you today?','Good, what is it that I can do to make you feel better?'],
             r'(.*)?(\s)?(sad|unhappy|worried|disturbed)':['Tell me why are you feeling %s?'],
             r'(.*) help':['Tell me how I can help you?', 'I am happy to help you'],
             r'i cannot (.*)':['Do you really cannot %s'],
             r'yes(.*)?(\s)?':['You seem to be knowing an answer.', 'Okay,can you please elaborate a bit?'],
             r'(.*)?(\s)?family(\s)?(.*)?':['Tell me more about your family.','What is your relationship with your family is like?',
                                  'How do you feel about your family?','Family relations are very important in ones life.'],
             r'(.*)?(\s)?sorry(\s)?(.*)?':['Please do not apologize to me.','Why did you feel like saying sorry?'],
             r'(.*)?(\s)?mother(\s)?(.*)?':['Tell me more about your mother.','What is your relationship with your mother is like?',
                                 'How do you feel about your mother?','Family relations are very important in ones life.'],
             r'(.*)?(\s)?father(\s)?(.*)?':['Tell me more about your father.','What is your relationship with your father is like?',
                                 'How do you feel about your father?','Family relations are very important in ones life.'],
             r'no(.*)?(\s)?':['May I know the reason?', 'Okay,can you please elaborate a bit?'],
             r'i need (.*)':['Could you please explain why you need %s?', 'Why do you need %s?', 'Are you sure that you need %s?'],
             r'i think (.*)':['Can you explain why do you think so?', 'Do you really think so?', 'Why are you not sure about it?'],
             r'because (.*)':['Do you think that is the only reason?', 'What other reasons came up to your mind?'],
             r'i like to (.*)':['Why do you like to %s?', 'Do you really like to %s?', 'Can you tell me more about why you like to %s?'],
             r'(.*)?(\s)?sleep(\s)?(.*)':['Can you tell me more about your sleeping pattern please','How many hours do you sleep?',
                                          'How often do you wake-up in sleep'],
             r'(.*)?(\s)?murder(\s)?(.*)':['Why do you have such a feeling?','That is not a solution to any problem', 'Please calm your mind'],
             r'(.*)?(\s)?hurt(\s)?(.*)':['Please calm your mind','Think of someone that you love','Stay positive'],
             r'(.*)?(\s)?eat(\s)?(.*)':['How many meals do you have in a day', 'What is your favourite food', 'Do you drink water after every meal'],
             r'(.*)?(\s)?angry(\s)?(.*)':['Please calm your mind','Take a deep breath'],
             r'(.*)?(\s)?suicide(\s)?(.*)':['Why did you feel like commiting?', 'I don’t think that is the only option you have','Do you want to explain further?']
             }
# creates a datetime object
x = datetime.datetime.now()
# extracting hours from datetime
hour = x.strftime("%H")
hours = int(hour)
# print welcome message based on time of day 
if (hours>=0 and hours<12):
  print('Good morning, I am ELIZA, your chatbot assistant.')
elif (hours>=12 and hours<16):
  print('Good afternoon, I am ELIZA, your chatbot assistant.')
elif (hours>=16 and hours<23):
  print('Good evening, I am ELIZA, your chatbot assistant.')
print('[Eliza] Hello, Please type in your name')
# grab the name of the user
user = input('[user] ')
tokens = nltk.word_tokenize(user)
name = tokens[-1]
# first message with user name
print('\n[Eliza] Hello %s, how are you today?' %name)
# exit list
exit = ['quit','bye','exit','good bye']
# salutation list
sal = ['hi','hello','hola']
# if any other key from responses is entered
empty = ['Can you please elaborate?', 'Okay,can you please elaborate a bit?','Interesting, please tell me more','Oh! I see. Please continue']
# final or quitting messages
quit_responses = ['Thank you for talking with me ','It has been a pleasure talking to you ','Bye. Please do not hesitate to come back again ',
                  'Good bye. Have a nice day ']
# improper language messages
bad = ['fuck','bitch','fuck off','shit']
list_empty = []
for i in responses.keys():
  list_empty.append(i)
# To auto stop if no input is entered for 20 seconds
def auto_stop():
  print("\n[Eliza] Are you still there? If yes please enter an input")
while True:
  # using timer function to count the wait time
  t = threading.Timer(20,auto_stop)
  t.start()
  inp = input('[%s] ' %name)
  t.cancel()
  chat = inp.lower()
  tokenizer = RegexpTokenizer(r'\w+')
  # tokenizing the chat
  chat_tokens = tokenizer.tokenize(chat)
  flag = 0
  length = len(list_empty)
  for i in list_empty:
   if not re.search(i,str(chat)):
    flag += 1
  flags = 0
  # improper language response
  if chat in bad:
    print('\n[Eliza] Please use a proper language')
 # if gibberish or not an english word is entered
  for chats in chat_tokens:
    if chats not in words.words() and chat not in bad:
      not_words = []
      flags+=1
      not_words.append(chats)
  if flags>0:
    unaware = ""
    # response for unaware words
    for i in not_words:
      unaware = unaware+" "+i
    print('\n[Eliza] I am sorry, I am unaware of the word'+unaware)
    # using wordnet to grab the meaning of the words
  if re.search('what is (.*)',str(chat)):
    syns = wordnet.synsets(chat_tokens[-1])
    print('\n[Eliza] '+syns[0].definition())
  if chat in exit:
    quitting = random.choice(quit_responses)
    print('\n[Eliza] '+quitting+ '%s.' %name)
    break  
    # if key is in salutations
  if chat in sal:
    print('\n[Eliza] Hello, how may I help you today %s?' %name)
  flagged = 0
  # using only alpha numeric characters
  if re.search('[^a-zA-Z0-9\s]',chat):
    flagged += 1
  if flagged>0:
      # response if other than alpha numeric characters are entered
    print('\n[Eliza] Please enter a valid input with only alphanumeric characters')
  if flag>length-1 and not re.search('what is (.*)',str(chat)) and flags<1 and chat not in sal and chat not in bad and flagged<1:
    value = random.choice(empty)
    print("\n[Eliza] "+value)
    # print responses if user's inputs in keys of responses 
  for keys,values in responses.items():
    temp = re.search(keys,str(chat))
    if temp:
      value = random.choice(values)
      replace = chat_tokens[-1]
      # grabbing response from question of the user
      if '%s' in value: 
        value = re.sub('%s',replace,value)         
        print("\n[Eliza] "+value)
        break
      else:
        print("\n[Eliza] "+value)
        break

