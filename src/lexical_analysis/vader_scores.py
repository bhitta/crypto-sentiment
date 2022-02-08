#!/usr/bin/env python3
import ast
import collections
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def score_dict_from_labels(label_path, freq_path, count_out_path):
    """
    takes csv with manual labels, file with common crypto words.
    outputs file with a dict of words and pos/neg occurences for manual cleanup.
    """
    labels = pd.read_csv(label_path)
    pos  = labels[labels["sentiment"] == 3.0]["PreprocessedTweetText"]
    neg  = labels[labels["sentiment"] == 1.0]["PreprocessedTweetText"]
    freq = pd.read_csv(freq_path).iloc[:, 0].tolist()
    fdict = dict.fromkeys(freq, 0)
    for tweet in pos:
        for word in ast.literal_eval(tweet):
            if word in fdict.keys():
                fdict[word] = fdict.get(word) + 1
    for tweet in neg:
        for word in ast.literal_eval(tweet):
            if word in fdict.keys():
                fdict[word] = fdict.get(word) - 1
    fdict = {key:val for key, val in fdict.items() if val != 0}

    with open(count_out_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in fdict.items():
            writer.writerow([key, value])


def clean_dict_to_vader_format(clean, neg, boost):
    score_df = pd.read_csv(clean, header=None)
    score_df = score_df.dropna()
    score_df.columns = ["token", "count"]
    score_df = score_df[score_df["token"].isin(neg) == False]
    score_df = score_df[score_df["token"].isin(boost) == False]
    max_val = max(score_df["count"])
    score_df["vader"] = score_df["count"].apply(lambda x: x / max_val * 4)
    return score_df

def plot_word_distribution(score_df, cut_off):
    dist = score_df["vader"].to_list()
    plt.hist(dist, bins=50)
    plt.gca().set(title="Vader Score Distribution", ylabel="# of score", xlabel="VADER score")
    plt.savefig("./data/posneg_words_vader.png")


def adjust_vader_lexicon(lexicon_path, score, out_path):
    """
    takes VADER lexicon and adds/adjusts entries according to score dict file.
    outputs adjusted VADER lexicon.
    """
    vader_v = pd.read_csv(lexicon_path, skiprows=[5, 1260, 2865, 5908], delim_whitespace=True, header = None)
    vader_v = vader_v.iloc[:, 0:2]
    vader_v.columns = ["token", "sentiment"]
    print(vader_v)


vanilla = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/vanilla/VANILLA_corpus_clean_combined.txt"

if __name__ == "__main__":
    label_path =  "/home/kw/projects/crypto-sentiment/data/twitter/manual_labelling_twitter.csv"
    freq_path =  "/home/kw/projects/crypto-sentiment/data/twitter/high_freq/high_frequency_words_CRYPTO.csv"
    count_out_path = f"/home/kw/projects/crypto-sentiment/data/twitter/pos_neg_occurence{datetime.now()}.csv"
    clean = "/home/kw/projects/crypto-sentiment/data/twitter/pos_neg_occurence_cleaned.csv"
    vader_van =  "/home/kw/projects/crypto-sentiment/data/twitter/vader_lexicon.txt"

    #TODO import these instead
    NEGATE = \
    ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
     "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
     "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
     "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
     "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
     "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
     "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
     "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]

    BOOSTER_DICT = \
    {"absolutely" , "amazingly" , "awfully" ,
     "completely" , "considerable" , "considerably" ,
     "decidedly" , "deeply" , "effing" , "enormous" , "enormously" ,
     "entirely" , "especially" , "exceptional" , "exceptionally" ,
     "extreme" , "extremely" ,
     "fabulously" , "flipping" , "flippin" , "frackin" , "fracking" ,
     "fricking" , "frickin" , "frigging" , "friggin" , "fully" ,
     "fuckin" , "fucking" , "fuggin" , "fugging" ,
     "greatly" , "hella" , "highly" , "hugely" ,
     "incredible" , "incredibly" , "intensely" ,
     "major" , "majorly" , "more" , "most" , "particularly" ,
     "purely" , "quite" , "really" , "remarkably" ,
     "so" , "substantially" ,
     "thoroughly" , "total" , "totally" , "tremendous" , "tremendously" ,
     "uber" , "unbelievably" , "unusually" , "utter" , "utterly" ,
     "very" ,
     "almost" , "barely" , "hardly" , "just enough" ,
     "kind of" , "kinda" , "kindof" , "kind-of" ,
     "less" , "little" , "marginal" , "marginally" ,
     "occasional" , "occasionally" , "partly" ,
     "scarce" , "scarcely" , "slight" , "slightly" , "somewhat" ,
     "sort of" , "sorta" , "sortof" , "sort-of" }

    #score_dict_from_labels(label_path, freq_path, count_out_path)
    score = clean_dict_to_vader_format(clean, NEGATE, BOOSTER_DICT)
    print(score.to_markdown())
    #plot_word_distribution(score, True)
    #adjust_vader_lexicon(vader_van, score, True)
