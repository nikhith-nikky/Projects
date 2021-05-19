# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 16:16:46 2020

@author: Nikhith
"""
# Author : Nikhith Theddu, Sumanth Bhargav Kanchi, Hemalekha Pillarishetty
# This program randomly generates sentences by taking the following inputs:
# 1. The value of n in n-grams
# 2. The number of sentences to be generated
# 3. The space separated names of text files
# Intially the algorithm reads the input files and all the files are combined to check whether the total number of tokens
# or words is greater than 10,00,000. If it is less than the required words, the code prompts a message saying 'Please input
# atleast 10,00,000 words'. If the n-grams is 1 then the frequency distribution of tokens is found and then the weighted frequency
# of the words is found by dividing every word frequecny with the maximum word frequecny. Then the sentence scores are calculated 
# by adding the weighted frequencies of each word in the sentence and sentences are ordered in descending order based on their scores
# With this a unigram model generates the required number of random sentences from the given text data. If ngrams is more than 1
# then the start and stop tags are appended to the sentences based on the value of n. Now the n-grams are created by joining the
# tokens based on the value of n. Now the n-1 grams are also created which can be used in generating the relative frequency table.
# In this algorithm only the words with a frequency of occurance are taken into a dictionary with keys as the ngram word and
# values as the next word with the value for that word as the frequency of occurance. Here the probability is generated by taking
# Markovian assumption into consideration. Initially the frequency of the predicted word is divided with the frequecny of the 
# corresponding key. Then normalization of the probabilities are done by dividing the intital probabilities with the sum of 
# probabilities of the corresponding ngram word. Now the process of sentence generation starts by choosing the start words and
# a random ngram is choosen from start words then a random number in the range of (0,1) is generated. If the random number lies
# in between the corresponding number line then it is chosen as the next word. Now this word is considered as the key for the next 
# word to be predicted. This process continues till an end of sentence is reached which is indicated by '.,!,?'. This process is
# done till the required number of sentences are printed.
# examples are given in the ngram-log.txt 
# In the first example less than 10,00,000 words are given and it thrown an error message 'Please input atleast 10,00,000 words'
# In the next examples Unigram, Bigram and Trigram models are used to generate 10 random sentences
# Additional functionality: Time taken to execute the program is calculated and printed in seconds.


import nltk
import re
import random
import sys
import heapq
import time
s = 'This program uses '+str(sys.argv[1])+'-grams to generate '+str(sys.argv[2])+' sentences'
# reading inputs from arguments
files = sys.argv[3:]
n = int(sys.argv[1])
sent_num = int(sys.argv[2])
text = ""
# combine all the files and convert text to lower case
for file in files:
    with open(str(file),'r',encoding='utf8') as f:
        text = text + f.read().lower()
# allowing only alpha numeric values and punctuations
clean_text = re.sub('[^0-9a-z \.\?!]',' ',text)
cleaned_text = re.sub(' +',' ',clean_text)
words = []
# word tokenization
tok = nltk.word_tokenize(cleaned_text)
SentTokens = nltk.sent_tokenize(cleaned_text)
# to record the time
start_time = time.time()
# to create a log file of commands executed
file = open("ngram-log.txt","a",encoding="utf-8")
argss = ""
for args in sys.argv[1:]:
    argss = argss+" "+str(args)
ss = 'Command line setting: pyhton ngram.py '+str(argss)
file.write(ss+'\n')
file.write(s+'\n')
s = 'Number of tokens is: '+str(len(tok))
print(s)
file.write(s+'\n')
# checking the word count
if len(tok)<1000000:
    s = 'Please input atleast 1,000,000 words'
    print(s)
    file.write(s+'\n')
    
else:
    # Unigram model
    if n == 1:
        freq_uni = nltk.FreqDist(tok)
        words_frequencies = []
        words_uni = []
        weighted = []
        # calculating word frequency
        for word_uni, frequency in freq_uni.items():
            words_frequencies.append(frequency)
            words_uni.append(word_uni)
        # calculating weighted frequency
        for word_uni, frequency in freq_uni.items():
            temp_uni = frequency/max(words_frequencies)
            weighted.append(temp_uni)
            final_weighted = {} 
        for key_uni in words_uni: 
            for value_uni in weighted: 
                final_weighted[key_uni] = value_uni 
                weighted.remove(value_uni) 
                break
        # calculating sentence scores and sentence generation
        sentence_scores = {}
        for sent in SentTokens:
            for word in nltk.word_tokenize(sent.lower()):
                if word in final_weighted.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = final_weighted[word]
                    else:
                        sentence_scores[sent] += final_weighted[word]
        # generating sentences based on the scores
        summary_sent = heapq.nlargest(sent_num, sentence_scores, key=sentence_scores.get)
        for i,j in enumerate(summary_sent):
            s = 'Sentence '+str(i+1)+': '+j
            print(s)
            file.write(s+'\n')
    else:
       # Ngram model
       sentences = nltk.sent_tokenize(cleaned_text)
       for sent in sentences:
           tokens = nltk.word_tokenize(sent)
           # appending the start tags
           if len(tokens) >= n:
               tokens.insert(0,'<s>')
               tokens.insert(len(tokens)-1,'</s>')
               words.append(tokens)
       total = []            
       for tot in words:
           for tal in tot:
               total.append(tal)

       n1grams = {}
       n1list = []
       # creating n-1 grams
       for word in words:    
           for j in range(len(word)):
               n1gram = ' '.join(word[j:j+n-1])
               n1list.append(n1gram)
        # frequency distribution of n-1 grams 
       freq = nltk.FreqDist(n1list)
       end = ['.','!','?']
       length = len(n1list)
       ngrams = {}
       # generating n-grams dictionary along with the frequency of next word
       for i in range(0, length - n):
           if n1list[i] in ngrams:
               if total[i + n-1] in ngrams[n1list[i]]:
                   ngrams[n1list[i]][total[i + n-1]] += 1
               else:
                   ngrams[n1list[i]][total[i + n-1]] = 1
           else:
               ngrams[n1list[i]] = {}
               ngrams[n1list[i]][total[i + n-1]] = 1
               
        # generating probabilities
       for keys,values in ngrams.items(): 
           for value,frequency in values.items():
               if freq[keys] == 0:
                   continue
               else:
                   values[value] = frequency/freq[keys]
        # normalizing the probabilities
       for keys,values in ngrams.items(): 
           sums = 0
           for value,frequency in values.items():
               sums = sums + values[value]
               values[value] = sums
       start = {}
       # start words
       for keys,values in ngrams.items():
           if '<s>' in keys:
               start[keys] = values
       count = 0       
       for sents in range(sent_num): 
           count += 1
           # choosing random start words
           star = random.choice(list(start.keys()))
           line = star
           while(True):
               temp = []
               for keys,values in ngrams.items():
                   # generating a random number
                   rand = random.random()
                   for value,frequency in values.items():
                       if star in keys:
                           if rand<values[value]:
                               temp.append(value)
                           else:
                               temp.append(random.choice(list(values.keys())))
               star = temp[0]
               line = line+" "+temp[0]
               if temp[0] in end:
                   break
           line = re.sub(r'(<s>|</s>)','',line)
           line = re.sub('  ','',line)
           # printing sentences
           s = 'Sentence '+str(count)+':'+line
           print(s)
           file.write(s+'\n')
end_time = time.time()
# printing time elapsed
s = 'Time elapsed: '+str(end_time-start_time)+' seconds'
print(s)
file.write(s+'\n\n')

