# analyze google searches to predict stock market
# remove tweets from other languages?
from __future__ import division
import tweepy
import shutil
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
# import matplotlib.pyplot as plt
import csv 
from textblob import TextBlob
import numpy as np
# from pylab import *
import os.path

access_token = "301847288-lWXEQAwNc7kvyIF4E6w3TCzj7FfWYyUs2FKXbkcR"
access_token_secret = "dXv1ktTNVsHVHsx7AUyVilLOx3tEWPc0Ffi8BvSh9VN10"
consumer_key = "MyrxJJIAAbIupjvNbqyUTzJOZ"
consumer_secret = "ZBZrMl7jEv1DGt76hCV60K7j8Z8uDx8K710cO1w6SBelNVSeqD"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class twitter_analyze:

	def __init__(self):
		pass
		
	# current feelings about stock
	# Todo plot according to location
	def analyze_feelings(self, stock):
		
		# tweets_file = 'data/%s_tweets.csv' %stock

		# if not os.path.isfile(tweets_file) : 
		tweets = self.analyze_stock(stock)
		
		# tweets = pd.read_csv('data/%s_tweets.csv' %stock)

		sentiment = []
		for index, row in tweets.iterrows():
			value = 0.0
			if isinstance(row['polarity'], float):
				value = round(row['polarity'], 3)
			else:
				x = float(row['polarity'])
				value = round(x, 3)
			if value < 0.0:
				sentiment.append('negative')
			elif value == 0.0:
				sentiment.append('neutral')
			else:
				sentiment.append('positive')

		tweets['sentiment'] = sentiment
		# tweets['sentiment'].value_counts().plot(kind='bar')
		# tweets['sentiment'].value_counts().plot(kind='pie')
		# plt.show()
		print tweets
		counts_list = []
		print tweets['sentiment'].value_counts()['positive']
		counts_list.append(tweets['sentiment'].value_counts()['positive'])
		counts_list.append(tweets['sentiment'].value_counts()['negative'])
		counts_list.append(tweets['sentiment'].value_counts()['neutral'])

		# file_feelings = ('data/%s_feelings.csv' % stock)
		# cur_path = os.getcwd()
		# abs_path_feelings = cur_path+'/'+file_feelings
		# with open(file_feelings, "w") as output:
		#     writer = csv.writer(output, lineterminator='\n')
		#     for val in counts_list:
		#         writer.writerow([val])  

		return counts_list
