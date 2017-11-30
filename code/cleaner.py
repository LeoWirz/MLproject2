# -*- coding: utf-8 -*-
"""
Class used to clean our data by removing words and/or regrouping them.
"""

class Cleaner:
    def __init__(self, stopWords = [], punctuation = []):
        """
        Stop words are to be ignored when dealing with a phrase.
        Punctuation need to be regrouped to form smileys that could be used for prediction.
        """
        self.stopWords = set(stopWords)
        self.punctuation = set(punctuation)
    
    def addStopWord(self, word):
        """
        Add exactly 1 word given as a string to stopWords.
        """
        self.stopWords.add(word)
    
    def addStopWords(self, words):
        """
        Add a list or set of words to stopWords.
        """
        self.stopWords = self.stopWords.union(set(words))
    
    def addPunctuation(self, punc):
        """
        Add exactly 1 element of punctuation given as a string to punctuation.
        """
        self.punctuation.add(punc)
    
    def addPunctuations(self, puncs):
        """
        Add a list or set of elements of punctuation to punctuation.
        """
        self.punctuation = self.punctuation.union(set(puncs))
    
    def removeStopWords(self, phrase):
        """
        Remove all stop words from the phrase given as a list.
        """
        phraseCopy = phrase.copy()
        for word in phraseCopy:
            if word in self.stopWords:
                phrase.remove(word)
        return phrase
    
    def isPunc(self, word):
        for char in word:
            if not(char in self.punctuation):
                return False
        return True
    
    def concatPunc(self, phrase):
        idx = 0     # We need to have a counter to explore the list that will be modified along the way
        
        while(idx < len(phrase)):
            if(self.isPunc(phrase[idx])):
                # While the word after the one we're looking at exist and is punctuation, we concat them
                while(not(idx == len(phrase)-1) and
                       self.isPunc(phrase[idx+1])):
                    phrase[idx] += phrase[idx+1]
                    del phrase[idx+1]
                
                if(len(phrase[idx]) == 1):  # We could also include punctuation of length 1 in stopWords
                    del phrase[idx]
                    continue    # In this case, we don't want to increment the index
            idx += 1
        
        return phrase
    
    def clean(self, data):
        """
        Perform removeStopWords and concatPunc on all the tweets from the data.
        Data is given as a list of tweets which are a list of strings
        """
        cleansedData = []
        for tweet in data:
            # Put all words to lowercase
            for i in range(len(tweet)):
                new_tweet = [c.lower()  for c in tweet]
            
            # Perform the 2 cleaning steps
            new_tweet = self.concatPunc(new_tweet)
            new_tweet = self.removeStopWords(new_tweet)
            cleansedData.append(new_tweet)
        
        return cleansedData