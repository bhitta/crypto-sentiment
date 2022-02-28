#!/usr/bin/env python3
import pandas as pd
import time
from statistics import mean
from datetime import datetime
from dateutil import parser
import multiprocessing as mp
import concurrent.futures
import sys
sys.path.append("/home/kw/projects/crypto-sentiment/")
from src.vaderSentiment.vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1: open twitter csv and adjust timestamps
#
def add_unix_time_col(twitter_csv, out_path):
    """
    add unix timestamp column to tweet_csvs used for correlative analysis
    """
    df = pd.read_csv(twitter_csv)
    df = df.dropna(subset=["created_at"])
    df["unix_time"] = df["created_at"].apply(lambda x: int(time.mktime(parser.parse(x).timetuple())) if x != "0" else None)
    df.to_csv(out_path, index=False)

def return_mean_sentiment(opn, cls):
    """
    takes open and close timestamp.
    returns mean score of tweets between open and close
    """
    # filter tweets for relevant candle

    tweet_set = twitter_df[twitter_df["unix_time"].between(opn, cls)]["text"]
    # run vader on all tweets in tweet
    mean_score = mean([classifier.polarity_scores(tweet)["compound"] for tweet in tweet_set])
    # append (opn,cls,mean_score) to sequence
    triple = {"open-time": opn, "close-time": cls, "mean_sentiment": mean_score}
    print(triple)
    seqproxy.append(triple)


def return_sentiment_sequence_parallel(candle_df, twitter_df, out_path):
    opns = [opn / 1000 for opn in candle_df["open-time"].to_list()]
    clss = [cls / 1000 for cls in candle_df["close-time"].to_list()]
    #parallelize here
    with concurrent.futures.ThreadPoolExecutor() as executor:
       data = executor.map(return_mean_sentiment, opns, clss)

if __name__ == "__main__":
    cashtag = "ATOM"
    candle_interval = "1h"
    classifier = SentimentIntensityAnalyzer()
    seqproxy = mp.Manager().list()
    candle_df = pd.read_csv(f"/home/kw/projects/crypto-sentiment/data/crypto/{cashtag}USDT-{candle_interval}-combined.csv")
    twitter_df  = pd.read_csv(f"/home/kw/projects/crypto-sentiment/data/twitter/processed/crypto/{cashtag}_2021_preprocessed_unix.csv")

    #add_unix_time_col(f"/home/kw/projects/crypto-sentiment/data/twitter/processed/crypto/{cashtag}_2021_preprocessed.csv", f"/home/kw/projects/crypto-sentiment/data/twitter/processed/crypto/{cashtag}_2021_preprocessed_unix.csv")
    #return_mean_sentiment(opn,cls)
    return_sentiment_sequence_parallel(candle_df, twitter_df, "")
    sequence_df = pd.DataFrame(list(seqproxy))
    sequence_df.to_csv(f"~/projects/crypto-sentiment/data/twitter/sentiment_sequences/sequence_{cashtag}_{candle_interval}.csv", index=False)
