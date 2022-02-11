import pandas as pd
import pickle
import os
import numpy as np


df = pd.read_pickle('/Users/ericschlosser/Desktop/TheHardWay/ISEEsite/ISEEsite/myproject/wordlists/df.pkl')
print('Before the update')
print(df.head())
df['Date'] = [np.nan]*499
wordlist = '/Users/ericschlosser/Desktop/TheHardWay/ISEEsite/ISEEsite/myproject/wordlists/df.pkl'
df.to_pickle(wordlist, compression = None)



print('We updated the pickle')
print(df.head())
