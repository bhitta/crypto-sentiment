#!/usr/bin/env python3

import os
import pandas as pd
from datetime import datetime
import ast

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


