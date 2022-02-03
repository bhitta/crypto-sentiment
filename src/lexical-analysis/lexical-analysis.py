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

    with open(out_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in crypto_specific.items():
            writer.writerow([key, value])


vanilla = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/vanilla/VANILLA_corpus_clean_combined.txt"
sol = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/SOL_corpus_clean.txt"
ftm = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/FTM_corpus_clean.txt"
atom = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/ATOM_corpus_clean.txt"
avax = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/AVAX_corpus_clean.txt"
crypto = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/crypto/CRYPTO_corpus_clean.txt"
freq_out = "/home/kw/projects/crypto-sentiment/data/twitter/corpora/high_frequency_words_SOL.csv"

if __name__ == "__main__":
    frequent_words(crypto, vanilla, freq_out, 500)
