#!/usr/bin/env python3
import pandas as pd


def man_label_sample(in_path, out_path, n_sample):
    """
    output csv for manual labelling task, randomly sampled from input csv.
    """
    df = pd.read_csv(in_path)
    df = df.sample(n_sample)
    df = df[["text", "PreprocessedTweetText"]]
    df.to_csv(out_path, index=False)

def sample_crypto_csv(ftm, avax, atom, sol, out, n_sample):
    """
    sample from crypto tweet csvs and output combined csv.
    """

    df_avax     = pd.read_csv(avax)
    avax_sample = df_avax.sample(n_sample)
    print(avax_sample.shape)

    df_ftm     = pd.read_csv(ftm)
    ftm_sample = df_ftm.sample(n_sample)
    print(ftm_sample.shape)

    df_atom     = pd.read_csv(atom)
    atom_sample = df_atom.sample(n_sample)
    print(atom_sample.shape)

    df_sol      = pd.read_csv(sol)
    sol_sample  = df_sol.sample(n_sample)
    print(atom_sample.shape)

    frames = [avax_sample, ftm_sample, atom_sample, sol_sample]
    result = pd.concat(frames)
    print(result.shape)

    result.to_csv(out, index=False)


if __name__ == "__main__":

    man_out  = "data/twitter/manual_labelling_twitter.csv"

    avax_csv = "data/twitter/raw/AVAX_2021.csv"
    ftm_csv  = "data/twitter/raw/FTM_2021.csv"
    atom_csv = "data/twitter/raw/ATOM_2021.csv"
    sol_csv  = "data/twitter/raw/SOL_2021.csv"
    sample_csv = "data/twitter/processed/crypto/CRYPTO_2021_preprocessed.csv"

    #sample_crypto_csv(ftm_csv, avax_csv, atom_csv, sol_csv, sample_csv, n_sample=250000)
    man_label_sample(sample_csv, man_out, 10000)
