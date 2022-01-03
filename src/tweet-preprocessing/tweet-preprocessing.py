#!/usr/bin/env python3
from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re,string

#uncomment below if running for the first time
#nltk.download('stopwords')

csv_path   = "./data/twitter/raw/$ETH OR Ethereum until:2021-11-30-raw-2021-12-08 11:59:08.021502.csv"
twt        = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)
spamwords  = ("giveaway", "bot", "crypto") #wie kann ich die liste finessen?
stop       = stopwords.words("english") + list(string.punctuation)
df         = pd.read_csv(csv_path)

def spam_word(tweet, spamwords):
    # drop row if tweet contains blacklisted term
    if any(word in tweet for word in spamwords):
        return True

def spam_tags(tweet, n_tags=8):
    # more than x tags in tweet should result in removal of tweet.
    counter = Counter(tweet)
    if counter["$"] >= n_tags or counter["#"] >= n_tags:
        return True

def drop_spam_row(tweet, index):
    # drop row if spam_word or spam_tags indicate spam
    if spam_word(tweet, spamwords) == True or spam_tags(tweet) == True:
        df.drop(index, inplace=True)
        return True

def strip_numbers(tweet):
    # many single numbers in the tweets. should delete
    return re.sub(r'\d+', '', tweet)

def strip_links(text):
    # strip urls from tweets
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def strip_all_entities(text):
    # strip @, #, $ tags from tweets
    entity_prefixes = ['@','#','$']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def preprocess_and_add_column(df):
    # drop unwanted rows, preprocess tweet text and return a new dataframe
    preprocessed = []
    for index, row in df.iterrows():
        tweet = row["TweetText"].lower()
        spamrow = drop_spam_row(tweet, index)
        if spamrow != True:
            tweet = strip_numbers(tweet)
            tweet = strip_links(tweet)
            tweet = strip_all_entities(tweet)
            tk_tweet = [token.lower() for token in twt.tokenize(tweet)
                        if token.lower() not in stop]
            if tk_tweet == []:
                tk_tweet = "NaN"
            preprocessed.append(tk_tweet)
    df["PreprocessedTweetText"] = preprocessed
    return df

def save_to_csv(df, csv_path):
    tmp_path = csv_path[:-4] + "-preprocessed" + csv_path[-4:]
    out_path = tmp_path.replace("raw", "processed")
    df.to_csv(out_path)

if __name__ == "__main__":
    preprocessed_df = preprocess_and_add_column(df)
    save_to_csv(preprocessed_df, csv_path)
