#!/usr/bin/env python3

import tweepy
from twitter_authentication import bearer_token
from datetime import datetime
import time
import pandas as pd
from pathlib import Path
import os

def scrape(ticker_tag, start_time, end_time, resume=False):
    client   = tweepy.Client(bearer_token, wait_on_rate_limit=True)
    filepath = f"./data/twitter/raw/{ticker_tag}_from_{start_time}_to_{end_time}_api.csv"
    if os.path.exists(filepath):
        filepath = filepath[:-4] + "-" + str(datetime.now()) + filepath[-4:]
    # if file exists, take tweet time of last tweet as start time
    if resume == True:
        start_time = ""

    tweets = []

    for response in tweepy.Paginator(client.search_all_tweets,
                                    query        = f"${ticker_tag} -is:retweet lang:en",
                                    user_fields  = ["username", "public_metrics", "description", "location"],
                                    tweet_fields = ["created_at", "geo", "public_metrics", "text"],
                                    expansions   = "author_id",
                                    start_time   = start_time,
                                    end_time     = end_time,
                                     max_results  = 500):
        time.sleep(1)
        df = flatten_to_dict(response)
        if os.path.isfile(filepath):
            df.to_csv(filepath, mode='a', index=False, header=False)
        else:
            df.to_csv(filepath, mode='w', index=False, header=True)
    return tweets

def flatten_to_dict(response):
    result = []
    user_dict = {}
    # Loop through each response object
    #for response in scraped_array:
    # Take all of the users, and put them into a dictionary of dictionaries with the info we want to keep
    for user in response.includes['users']:
        user_dict[user.id] = {'username': user.username,
                            'followers': user.public_metrics['followers_count'],
                            'tweets': user.public_metrics['tweet_count'],
                            'description': user.description,
                            'location': user.location
                            }
    for tweet in response.data:
        # For each tweet, find the author's information
        author_info = user_dict[tweet.author_id]
        # Put all of the information we want to keep in a single dictionary for each tweet
        result.append({'author_id': tweet.author_id,
                    'username': author_info['username'],
                    'author_followers': author_info['followers'],
                    'author_tweets': author_info['tweets'],
                    'author_description': author_info['description'],
                    'author_location': author_info['location'],
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count'],
                    'likes': tweet.public_metrics['like_count'],
                    'quote_count': tweet.public_metrics['quote_count']
                    })

    # Change this list of dictionaries into a dataframe
    df = pd.DataFrame(result)
    return df

ticker_tag = "SOL"
tweets     = scrape(ticker_tag,  start_time = "2021-01-01T00:00:00Z", end_time =  "2021-12-31T23:59:59Z")
#df         = flatten_to_dict(tweets)
