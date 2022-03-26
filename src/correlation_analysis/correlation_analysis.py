#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

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

def crosscorr(series_a, series_b, lag=0):
    """
    Pearson cross-correlation with lag.
    second input array is shifted according to lag (pos/neg possible).
    """
    return series_a.corr(series_b.shift(lag))

def plot_crosscor_graph(cashtag, interval, out):
    """
    outputs crosscor graph for report for cryptocurrency and candle interval
    """
    xcor_vol = [crosscorr(tv, pc, lag=i) for i in lag]
    xcor_sent = [crosscorr(ms, pc, lag=i) for i in lag]


    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, ncols=1)
    fig.suptitle(f"{cashtag} {interval}")

    ax1.plot(o)
    ax1.set_title("Price in USD")
    ax1.set_yscale("log")
    ax1.set_ylabel("Price in USD")
    ax1.set_xlabel(f"# of {interval} candles in 2021")

    ax2.plot(tv)
    ax2.set_title("Tweet Volume")
    ax2.set_yscale("log")
    ax2.set_ylabel("# of Tweets per candle")
    ax2.set_xlabel(f"# of {interval} candles in 2021")

    ax3.plot(ms)
    ax3.set_title("Tweet Mean Sentiment")
    ax3.set_yscale("log")
    ax3.set_ylabel("mean VADER score per candle")
    ax3.set_xlabel(f"# of {interval} candles in 2021")

    ax4.stem(lag, xcor_vol)
    ax4.set_xlabel(f"timelag in {interval}")
    ax4.set_ylabel("correlation score")
    ax4.set_xticks(lag)
    ax4.set_title("Time-lagged Cross-Correlation: Price Change x Tweet Volume")

    ax5.stem(lag, xcor_sent)
    ax5.set_xlabel(f"timelag in {interval}")
    ax5.set_ylabel("correlation score")
    ax5.set_xticks(lag)
    ax5.set_title("Time-lagged Cross-Correlation: Price Change x Sentiment")

    plt.tight_layout()
    fig.subplots_adjust(hspace=0.7)
    fig.set_figheight(15)
    fig.set_figwidth(15)

    plt.savefig(f"./data/crosscorr{cashtag}_{interval}_{lag}")

    #print(xcor_daily)

if __name__ == "__main__":
    cashtag = "ATOM"
    interval = "1h"
    lag = range(-12,13)

    candles = f"/home/kw/projects/crypto-sentiment/data/crypto/{cashtag}USDT-{interval}-combined.csv"
    candle_df = pd.read_csv(candles)

    sentiment = f"/home/kw/projects/crypto-sentiment/data/twitter/sentiment_sequences/sequence_{cashtag}_{interval}.csv"
    sent_df = pd.read_csv(sentiment)

    combined_df = create_price_pcnt_sent_df(sent_df, candle_df)
    combined_df.to_csv(f"/home/kw/projects/crypto-sentiment/data/combined/{cashtag}_{interval}_combined.csv")

    tv = combined_df["tweet-volume"]
    pc = combined_df["percent-change"]
    ms = combined_df["mean_sentiment"]
    o = combined_df["open"]

    plot_crosscor_graph(cashtag, interval)
