#!/usr/bin/env python3

from bs4 import BeautifulSoup
import pandas as pd
import requests, zipfile, io, dryscrape, time, argparse, os, glob

parser = argparse.ArgumentParser(description="Choose Binance Trading Pair and Candle Interval")
parser.add_argument('-p', '--pair', required=True, help="Binance Trading Pair")
parser.add_argument('-i', '--interval', required=True, help="Candle Interval")
parser.add_argument('-o', '--output', default=f"./data/crypto", help="Output Directory")
args = parser.parse_args()

def download_monthly_csvs(pair, interval, output_dir):
    new_path = os.path.join(output_dir, f"{pair}-{interval}-raw")
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    url = f"https://data.binance.vision/?prefix=data/spot/monthly/klines/{pair}/{interval}/"
    print(f"Visiting {url} ...")
    session = dryscrape.Session()
    session.visit(url)
    time.sleep(5)
    response = session.body()
    soup     = BeautifulSoup(response, features="lxml")
    links    = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if any(href.endswith(x) for x in ['.zip']):
            zip_file_url = href
            r = requests.get(zip_file_url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(new_path)
            print(f"Downloaded {href} to {new_path} !")

def append_csvs(pair, interval, csv_dir):
    head = ["open-time", "open", "high", "low", "close", "volume", "close-time", "quote-asset-volume", "no-trades", "taker-buy-base-asset-volume", "taker-buy-quote-asset-volume", "ignore"]
    new_path = os.path.join(csv_dir, f"{pair}-{interval}-raw")
    all_files = glob.glob(new_path + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, names=head)
        li.append(df)
    print("Appending raw files to one large file")
    vertical_stack = pd.concat(li)
    vertical_stack.reset_index(drop=True, inplace=True)
    vertical_stack.to_csv(os.path.join(csv_dir, f"{pair}-{interval}-combined.csv"))
    print("Saving ... Done")

download_monthly_csvs(args.pair, args.interval, output_dir=args.output)
append_csvs(args.pair, args.interval, csv_dir=args.output)
