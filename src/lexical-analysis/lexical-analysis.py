#!/usr/bin/env python3
import ast
import collections
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def frequent_words(crypto_path, vanilla_path, out_path, n_top):
    vanilla = ast.literal_eval(open(vanilla_path).read())
    crypto     = ast.literal_eval(open(crypto_path).read())
    vanilla_count = dict(collections.Counter(vanilla).most_common(n_top))
    crypto_count     = dict(collections.Counter(crypto).most_common(n_top))
    crypto_specific = dict(set(crypto_count.items()) - set(vanilla_count.items()))

    #df = pd.DataFrame.from_dict(ftm_specific, orient="index")
    #df.to_csv(out_path, header=["Word", "Count"])
    #pd.DataFrame(ftm_specific).T.reset_index().to_csv(out_path, header=False, index=False)
    with open(out_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in crypto_specific.items():
            writer.writerow([key, value])



vanilla = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/vanilla/VANILLA_corpus_clean_combined.txt"
crypto = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/SOL_corpus_clean.txt"
out = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/high_frequency_words_SOL.csv"

if __name__ == "__main__":
    frequent_words(crypto, vanilla, out, 500)

#tfIdfVectorizer = TfidfVectorizer(use_idf=True)

#vectorizer      = tfIdfVectorizer
#X               = vectorizer.fit_transform(vanilla)
#feature_names   = vectorizer.get_feature_names_out()
#feature_names = vectorizer.get_feature_names_out()

#df              = pd.DataFrame(tfidf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
#df_sort         = df.sort_values("TF-IDF", ascending=False)
#print(df_sort.head(25))
