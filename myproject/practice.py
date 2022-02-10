import pandas as pd
import pickle
import os

df = pd.read_excel('/Users/ericschlosser/Desktop/TheHardWay/ISEEsite/ISEEsite/myproject/wordlists/ISEEWords1 3.xlsx', parse_dates = ['Date'])
wordlist_path = os.path.join('/Users/ericschlosser/Desktop/TheHardWay/ISEEsite/ISEEsite/myproject/wordlists', 'twowordlist_pickle.pkl')
#wordlist_filename = str(self.username) + '_wordlist'
pickle.dump(df, open(wordlist_path, 'wb'))

print(df.head())

df = pickle.load(open('/Users/ericschlosser/Desktop/TheHardWay/ISEEsite/ISEEsite/myproject/wordlists/twowordlist_pickle.pkl', 'rb'))

print(df)
