#!/usr/bin/env python3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

data = ["You need to be buying YAYO. You need to be accumulating. You need to be building your stack constantly. Sports cars, cocaine, assault weapons, super models, expensive watches, car phones, money. You need to be rich."] #open csv and append all strings in processed column

tfIdfVectorizer = TfidfVectorizer(use_idf=True)
tfidf = tfIdfVectorizer.fit_transform(data)
df = pd.DataFrame(tfidf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
df = sort_values("TF-IDF", ascending=False)
print(df.head(25))
