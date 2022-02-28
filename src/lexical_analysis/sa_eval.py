#!/usr/bin/env python3
import pandas as pd
from sklearn.metrics import accuracy_score
import sys

sys.path.append("/home/kw/projects/crypto-sentiment/")
from src.vaderSentiment.vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_score(tweet):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(tweet)

    if sentiment_dict["compound"] >= 0.05:
        result = 3
    elif sentiment_dict["compound"] <= - 0.05:
        result = 1
    else:
        result = 2
    return result

def tweet_sentiment_acc_score(label_csv):
    labels = pd.read_csv(label_csv)
    labels = labels[labels["sentiment"].notna()]
    labels["vanilla_pred"] = labels["text"].apply(lambda x: sentiment_score(x))
    gold = labels["sentiment"].to_list()
    pred = labels["vanilla_pred"].to_list()
    acc_score = accuracy_score(gold, pred)
    return acc_score



if __name__ == "__main__":
    label_path =  "/home/kw/projects/crypto-sentiment/data/twitter/manual_labelling_twitter.csv"
    acc = tweet_sentiment_acc_score(label_path)
    print(acc)
