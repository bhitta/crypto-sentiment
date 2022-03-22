#!/usr/bin/env python3
import sys
sys.path.append("/home/kw/projects/crypto-sentiment/")

import ast
import collections
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from src.lexical_analysis.sa_eval import sentiment_score


def score_dict_from_labels(label_path, freq_path, count_out_path, train_test_split):
    """
    takes csv with manual labels, file with common crypto words.
    outputs file with a dict of words and pos/neg occurences for manual cleanup.
    """
    labels = pd.read_csv(label_path)
    labels = labels.iloc[: int(train_test_split * len(labels))]
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

#def scale_up(x):
#    #return x*(1 + save_max - x)
#    return x * (1 + (max_val - x)/max_val)

#def normalize_for_vader(x):
#    return x  / max_val  * 4


def clean_dict_to_vader_format(clean, neg, boost):
    score_df = pd.read_csv(clean, header=None)
    score_df = score_df.dropna()
    score_df.columns = ["token", "count"]
    score_df = score_df[score_df["token"].isin(neg) == False]
    score_df = score_df[score_df["token"].isin(boost) == False]
    score_df_pos = score_df.loc[score_df["count"] > 15 ]
    score_df_neg = score_df.loc[score_df["count"] < -1 ]
    score_df =  pd.concat([score_df_pos, score_df_neg])
    score_df["vader"] = 0
    score_df["vader"][score_df["count"] >= 50] = 4
    score_df["vader"][score_df["count"] <  50] = 3
    score_df["vader"][score_df["count"] <  20] = 2
    score_df["vader"][score_df["count"] <  -2] = -2
    score_df["vader"][score_df["count"] <  -5] = -3
    score_df["vader"][score_df["count"] <  -9] = -4
    #max_val = max(score_df["count"])
    #score_df["vader"] = score_df["count"].apply(lambda x: x * (1 + (max_val -x) / max_val))
    #score_df["vader"] = score_df["count"].apply(lambda x: x * (1 + max_val - x))
    #score_df["vader"] = score_df["vader"].apply(lambda x: x  / max_val  * 4)
    return score_df

def plot_word_distribution(score_df, cut_off):
    dist = score_df["count"].to_list()
    plt.hist(dist, bins=50)
    plt.gca().set(title="PosNeg Score Distribution", ylabel="# of score", xlabel="PosNeg score")
    plt.savefig("./data/posneg_words_posneg_score.png")

def plot_sentiment_proportions(label_csv, preds):
    labels = pd.read_csv(label_csv)
    if preds:
        labels["vanilla_pred"] = labels["text"].apply(lambda x: sentiment_score(x))
        pos  = len(labels[labels["vanilla_pred"] == 3.0])
        neg  = len(labels[labels["vanilla_pred"] == 1.0])
        neu  = len(labels[labels["vanilla_pred"] == 2.0])
        title = "Predicted Tweets Sentiment Proportions with edited VADER Lexicon"
        out = "./data/predicted_sentiment_proportions_edited.png"
    else:
        pos  = len(labels[labels["sentiment"] == 3.0])
        neg  = len(labels[labels["sentiment"] == 1.0])
        neu  = len(labels[labels["sentiment"] == 2.0])
        title = "Labelled Tweets Sentiment Proportions"
        out = "./data/gold_sentiment_proportions.png"

    total = sum([pos, neg, neu])
    sizes = [pos/total, neg/total , neu/total]
    labels_arr = ["Positive", "Negative", "Neutral"]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels_arr, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')
    plt.gca().set(title=title)
    plt.savefig(out)

def adjust_vader_lexicon(lexicon_path, score, out_path):
    """
    takes VADER lexicon and adds/adjusts entries according to score dict file.
    outputs adjusted VADER lexicon.
    """
    vader_v = pd.read_csv(lexicon_path, sep="\t", header = None)
    vader_v.columns = ["token", "sentiment", "sd", "ratings"]
    print(vader_v.shape)
    for (idx, token, count, vader) in score.itertuples():
        if vader > 0.5 or vader < 0:
            if token in vader_v["token"].to_list():
                vader_v.loc[vader_v["token"] == token, "sentiment"] = vader
            else:
                vader_v = vader_v.append({"token": token, "sentiment": vader}, ignore_index=True)
    vader_v.to_csv(out_path, sep="\t", index=False, header=None)


vanilla = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/vanilla/VANILLA_corpus_clean_combined.txt"

if __name__ == "__main__":
    train_test_split = 0.8
    label_path =  "/home/kw/projects/crypto-sentiment/data/twitter/manual_labelling_twitter.csv"
    freq_path =  "/home/kw/projects/crypto-sentiment/data/twitter/high_freq/high_frequency_words_CRYPTO.csv"
    count_out_path = f"/home/kw/projects/crypto-sentiment/data/twitter/pos_neg_occurence{datetime.now()}.csv"
    clean = "/home/kw/projects/crypto-sentiment/data/twitter/pos_neg_occurence_cleaned.csv"
    vader_van =  "/home/kw/projects/crypto-sentiment/data/twitter/lexica/vader_lexicon.txt"
    vader_out =  "/home/kw/projects/crypto-sentiment/data/twitter/lexica/vader_lexicon_edited.txt"

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

    #score_dict_from_labels(label_path, freq_path, count_out_path, train_test_split)
    #score = clean_dict_to_vader_format(clean, NEGATE, BOOSTER_DICT)
    #print(score.to_markdown())
    #plot_word_distribution(score, True)
    #adjust_vader_lexicon(vader_van, score, vader_out)
    plot_sentiment_proportions(label_path, preds=True)
