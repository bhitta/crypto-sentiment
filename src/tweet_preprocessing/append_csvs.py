#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import ast, csv, os

def append_csvs(in_dir, out_path):
    df = pd.DataFrame([])
    for file in os.listdir(in_dir):
        df_new = pd.read_csv(os.path.join(in_dir, file))
        print(df_new.shape)
        df = pd.concat([df, df_new])

    df.to_csv(out_path + "VANILLA_2021_06-preprocessed_combined.csv")

    return df

def append_corpora(in_dir, out_path):
    out_list = []
    for file in os.listdir(in_dir):
        corp_file = open(os.path.join(in_dir, file))
        corp_part = ast.literal_eval(corp_file.read())
        out_list = out_list + corp_part

    with open(out_path + "VANILLA_corpus_clean_combined.txt", "w+") as output:
        output.write(str(out_list))

def lenght_reader(atom, avax, ftm, sol):
    """
    takes tweet csv filepaths and prints length.
    """
    f_a = open(avax, "r+")
    reader_a = csv.reader(f_a)
    value_a = len(list(reader_a))
    print(f"{value_a} tweets for avalanche in 2021.")

    f_f = open(ftm, "r+")
    reader_f = csv.reader(f_f)
    value_f = len(list(reader_f))
    print(f"{value_f} tweets for fantom in 2021.")

    f_at = open(atom, "r+")
    reader_at = csv.reader(f_at)
    value_at = len(list(reader_at))
    print(f"{value_at} tweets for atom in 2021.")

    f_s = open(sol, "r+")
    reader_s = csv.reader(f_s)
    value_s = len(list(reader_s))
    print(f"{value_s} tweets for solana in 2021.")
