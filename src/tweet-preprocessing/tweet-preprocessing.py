#!/usr/bin/env python3
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import itertools
from datetime import datetime

#uncomment below if running for the first time
#nltk.download('stopwords')

def save_text_corpus(corpus, output_path, cashtag, timestamp):
    # get aggregated tweets and save to txt file
    filepath = output_path + f"{cashtag}_corpus_clean_{timestamp}.txt"
    with open(filepath, "w+") as output:
        output.write(str(list(itertools.chain(*corpus))))

def save_to_csv(df, csv_path, timestamp):
    tmp_path = csv_path[:-4] + f"-preprocessed_{timestamp}" + csv_path[-4:]
    out_path = tmp_path.replace("raw", "processed")
    df.to_csv(out_path, index=False)

def preprocess_and_add_column(df, cashtag, csv_path):
    # drop unwanted rows, preprocess tweet text and return a new dataframe
    df["text"] = df["text"].str.lower()
    df = df[~df["text"].str.contains('|'.join(spamwords), na=False)]
    df = df[(df["text"].str.count("#") <= 8) | (df["text"].str.count("$") <= 8) | (df["text"].str.count("@") <= 8)]
    preprocessed = df['text'].replace(r'http\S+|\$\S+|\#\S+|\@\S+|[0-9.,$&:;?@#><*()%!-]|\n', '', regex=True)
    preprocessed = preprocessed.apply(lambda tweet: twt.tokenize(tweet) if type(tweet) == str else "")
    preprocessed = preprocessed.apply(lambda tweet: [word for word in tweet if word not in (stop)])
    df["PreprocessedTweetText"] = preprocessed

    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    corpus = save_text_corpus(preprocessed, "/home/kw/projects/crypto-sentiment/data/twitter/corpora/", cashtag, timestamp)
    save_to_csv(df, csv_path, timestamp)

if __name__ == "__main__":

    cashtag = "VANILLA"
    csv_path   = f"./data/twitter/raw/{cashtag}_2021_09.csv"
    twt        = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)
    spamwords  = ("giveaway", "bot", "crypto", "whitelist") #wie kann ich die liste finessen?
    stop       = stopwords.words("english") + list(string.punctuation)
    df         = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip", engine="python")
    #df_test    = pd.read_csv(csv_path).iloc[:20]

    preprocess_and_add_column(df, cashtag, csv_path)
