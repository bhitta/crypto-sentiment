#!/usr/bin/env python3
import pandas as pd

man  = "data/twitter/raw/manual_labelling_twitter.csv"

avax = "data/twitter/raw/AVAX_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
ftm  = "data/twitter/raw/FTM_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
atom = "data/twitter/raw/ATOM_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"
sol  = "data/twitter/raw/SOL_from_2021-01-01T00:00:00Z_to_2021-12-31T23:59:59Z_api.csv"

df_avax     = pd.read_csv(avax)
avax_sample = df_avax.sample(800)

df_ftm     = pd.read_csv(ftm)
ftm_sample = df_ftm.sample(800)

df_atom     = pd.read_csv(atom)
atom_sample = df_atom.sample(800)

df_sol      = pd.read_csv(sol)
sol_sample  = df_sol.sample(800)

frames = [avax_sample, ftm_sample, atom_sample, sol_sample]
result = pd.concat(frames)["text"]

result.to_csv(man, sep='\t')
