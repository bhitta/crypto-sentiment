#!/usr/bin/env python3
from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re,string

nltk.download('stopwords')

# remove bot tweets with certain words: giveaway, bot
# remove twitter tags #,@,$
# lower case
# tokenization
# remove stop words
# lemmatization

csv_path = "./data/twitter/raw/$ETH OR Ethereum until:2021-11-30-raw-2021-12-08 11:59:08.021502.csv"
output_path = "./data/twitter/processed/"
twt = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)

spamwords = ("giveaway", "bot", "crypto") #wie kann ich die liste finessen?
stop = stopwords.words("english") + list(string.punctuation)

df = pd.read_csv(csv_path)

def spam_word(tweet, spamwords):
    if any(word in tweet for word in spamwords):
        return True

def spam_tags(tweet, n_tags=8):
    #more than x tags in tweet should result in removal of tweet.
    counter = Counter(tweet)
    if counter["$"] >= n_tags or counter["#"] >= n_tags:
        return True

def drop_spam_row(tweet, index):
    # drop row if spam_word or spam_tags indicate spam
    if spam_word(tweet, spamwords) == True or spam_tags(tweet) == True:
        df.drop(index, inplace=True)

def strip_numbers(tweet):
    # many single numbers in the tweets. should delete
    return re.sub(r'\d+', '', tweet)


def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def strip_all_entities(text):
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

for index, row in df.iterrows():
    tweet = row["TweetText"].lower()
    print(tweet)
    drop_spam_row(tweet, index)
    tweet = strip_numbers(tweet)
    tweet = strip_links(tweet)
    tweet = strip_all_entities(tweet)
    tk_tweet = [token.lower() for token in twt.tokenize(tweet)
                if token.lower() not in stop]
    print(tk_tweet)
print(df.shape)
