# -*- coding: utf-8 -*-
"""
Script regrouping useful functions to import the data, clean it, save the result of a computation....
"""

from enum import Enum
import math

# Class that describes the sentiment of a tweet.
class Sentiment(Enum):
    NEGATIVE = -1
    POSITIVE =  1


##############################
### DATA RELATED FUNCTIONS ###
##############################

def load_data(file_path):
    """
    Reads a binary file containing tweets and return a list of usable strings.
    """
    file = open(file_path, "rb")
    tweets = []
    
    while(True):
        tweet = file.readline().decode("utf-8")
        if(tweet == ""):   # EOF
            break
        
        tweet = tweet[:-1]  # Remove the \n
        tweets.append(tweet)    # We want to store a list of words
    
    file.close()
    print("Successfully loaded data from " + file_path)
    return tweets


def load_training_data(file_path):
    """
    The training data doesn't have any IDs, so we can simply use it like that.
    """
    return load_data(file_path)

def load_test_data(file_path):
    """
    For the test data, we need to remove the IDs at the start of each line.
    """
    id_tweets = load_data(file_path)
    tweets = []
    
    for tweet in id_tweets:
        tweet = tweet.split(",", 1)[1]  # Remove the id as it corresponds to its place in the list
        # Note that the IDs start at 1, whereas indexation in Python starts at 0 !!!
        
        tweets.append(tweet)
    
    return tweets

def create_submission(name, results):
    """
    Create a csv file named "name.csv" regrouping the results in the provided list,
        ordered the same way as it was given at the start.
    Note that the results should be -1 or 1.
    """
    if name[-4:] != ".csv":
        file_path = name + ".csv"
    else:
        file_path = name
    
    file = open(file_path, "w")
    
    id = 0
    file.write("Id,Prediction\n")   # Header
    
    # Write each result one by one
    for result in results:
        id += 1
        line = str(id) + "," + str(result) + "\n"
        file.write(line)
    
    file.close()
    print("File " + file_path + " succesfully created with " + str(id) + " entries")


########################
### CROSS-VALIDATION ###
########################

def load_data_for_cross_validation(file_path, N, sentiment):
    """
    We load the training data as usual, but take away the last N tweets to be used for cross-validation.
    """
    tweets = load_data(file_path)
    return tweets[:-N], tweets[-N:], [sentiment for x in range(N)]

def cross_validation_results(results, reality):
    """
    Return the percentage of similitude between results and reality.
    """
    length = len(results)
    if length != len(reality):
        return 0

    sim = 0
    for i in range(length):
        if results[i] == reality[i]:
            sim += 1
    
    return 100*sim/length


###############################
### MATH AND MISC FUNCTIONS ###
###############################

def sigmoid(weight, sigmoid_coef):  
    # Return a function of the weight s.t. weights near 1 or -1 are nearer to them, and so do values near 0
    # NB : we use an odd power function on [0,1] and its reflection on [-1,0]
    if weight < 0:
        coef = -1
    else:
        coef = 1
    
    return coef * (my_power(2*abs(weight)-1,sigmoid_coef)+1)/2

def my_power(x, y):
    if x >= 0:
        return x**y
    else:
        return -(-x)**y

def update_progress(progress, total_size, precision, phase):
    if(progress % (math.floor(total_size/precision)) == 0):
        print(phase + " : " + str(100*progress/total_size) + "%  ", end="\r")
    return progress + 1