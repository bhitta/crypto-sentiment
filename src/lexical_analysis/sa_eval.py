#!/usr/bin/env python3
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import sys

sys.path.append("/home/kw/projects/crypto-sentiment/")
from src.vaderSentiment.vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_score(tweet):
    """
    used vader to classify tweet into pos, neg, neutral classes.
    """
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(tweet)

    if sentiment_dict["compound"] >= 0.05:
        result = 3
    elif sentiment_dict["compound"] <= - 0.05:
        result = 1
    else:
        result = 2
    return result

def tweet_sentiment_acc_score(label_csv, train_test_split):
    """
    takes gold standard label csv.
    outputs confusion matrix and accuracy score for test set.
    """
    labels = pd.read_csv(label_csv)
    labels = labels[labels["sentiment"].notna()]
    labels = labels.iloc[int(train_test_split * len(labels)) :]
    labels["vanilla_pred"] = labels["text"].apply(lambda x: sentiment_score(x))
    gold = labels["sentiment"].to_list()
    pred = labels["vanilla_pred"].to_list()
    matrix = confusion_matrix(gold, pred)
    matrix.diagonal()/matrix.sum(axis=1)
    print(matrix)
    df_cm = pd.DataFrame(matrix, index = ["neg", "neutr", "pos"],
                  columns = ["neg", "neutr", "pos"])
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)
    plt.savefig("/home/kw/projects/crypto-sentiment/data/twitter/confusion_matrix_vader_vanilla.png")
    acc_score = accuracy_score(gold, pred)
    return acc_score



if __name__ == "__main__":
    train_test_split = 0.8
    label_path =  "/home/kw/projects/crypto-sentiment/data/twitter/manual_labelling_twitter.csv"
    acc = tweet_sentiment_acc_score(label_path, train_test_split)
    print(acc)
