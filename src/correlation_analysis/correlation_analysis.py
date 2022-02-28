#!/usr/bin/env python3

import pandas as pd

def create_price_pcnt_sent_df(sent_df, candle_df):
    """
    receives: sentiment sequence df, market data df.
    returns: df with temporally-corresponding columnds for sentiment
    scores and percent price changes.
    """
    first_open = sorted(sent_df["open-time"])[0] * 1000 # milliseconds
    last_open = sorted(sent_df["open-time"])[-1] * 1000 # milliseconds
    candle_df = candle_df[candle_df["open-time"].between(first_open, last_open)]
    candle_df["open-time"] = candle_df["open-time"].apply(lambda x: int(x / 1000))
    candle_df["percent-change"] = candle_df["open"].pct_change()
    append_df = candle_df[["open-time", "open", "high", "low", "close", "volume", "percent-change"]]
    combined_df = sent_df.join(append_df.set_index("open-time"), on="open-time")
    return combined_df



if __name__ == "__main__":
    cashtag = "ATOM"
    interval = "1h"

    candles = f"/home/kw/projects/crypto-sentiment/data/crypto/{cashtag}USDT-{interval}-combined.csv"
    candle_df = pd.read_csv(candles)

    sentiment = f"/home/kw/projects/crypto-sentiment/data/twitter/sentiment_sequences/sequence_{cashtag}_{interval}.csv"
    sent_df = pd.read_csv(sentiment)

    combined_df = create_price_pcnt_sent_df(sent_df, candle_df)
    combined_df.to_csv(f"/home/kw/projects/crypto-sentiment/data/combined/{cashtag}_{interval}_combined.csv")
