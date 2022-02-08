#!/usr/bin/env python3

import csv

avax = "data/twitter/raw/AVAX_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
ftm  = "data/twitter/raw/FTM_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
atom = "data/twitter/raw/ATOM_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
sol  = "data/twitter/raw/SOL_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"

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
