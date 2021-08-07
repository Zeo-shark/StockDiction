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

