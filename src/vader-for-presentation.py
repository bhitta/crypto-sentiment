#!/usr/bin/env python3
import nltk
#nltk.download('vader_lexicon') # uncomment if first using vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

t1 = """ hope all you people selling $movr are just trying to
        get a better position otherwise you ngmi. hodl this gem to
        financial freedom. imagine being this early on $eth """

ps1 = sid.polarity_scores(t1)

t2 = " $QRDO very close neck breaking fomo pump. "

ps2 = sid.polarity_scores(t2)

t3 = """ we are obviously getting closer to a real bottom
        and we are obviously getting closer to a bullish momentum
        this is the time where you buy if you can hold like you should
        paper hands will ngmi """

ps3 = sid.polarity_scores(t3)

t4 = """ dear #shibarmy, whales, coyotes fear salip, they are releasing
        fomo to get your $shibs. do not be afraid. take care of your property patiently.
        don't panic. be patient, stand up straight. the pump is close.
        patience is the key to everything. it opens the door. """

ps4 = sid.polarity_scores(t4)

t5 = """ $KIBA on fire
        we had a breakout from the ascending channel a short retest followed by the pump to ath
        don't sleep on this beast you will be left behind to fomo waiting for a dip
        that isn't coming. """

ps5 = sid.polarity_scores(t5)


t6 = """ #bitcoin rallies over 60% in 5 weeks and takes a breather
        and the bears come out? if you are bearish rn you are ngmi.
        zoom out. stack and hodl. """

ps6 = sid.polarity_scores(t6)


t7 = """ $ftm about to go on sale?
head & shoulders 4h chart looking nasty tbh.
still stand by my statement: confident $ftm
will be a top 20 project,
meaning 2-3x from current price
short term price movements irrelevant if you believe this ^^ """

ps7 = sid.polarity_scores(t7)

t8 = """ $shiba rugpull in full effect, when will you people learn. """

ps8 = sid.polarity_scores(t8)


t9 = """ $aaa gonna pump to the moon """

ps9 = sid.polarity_scores(t9)

list = ([t1, ps1], [t2, ps2], [t3, ps3], [t4, ps4], [t5, ps5], [t6, ps6], [t7, ps7], [t8, ps8], [t9, ps9])

for x,y in list:
    print("Tweet: " + x)
    print(" ")
    print("Sentiment scores: " + str(y))
    print(" ")
