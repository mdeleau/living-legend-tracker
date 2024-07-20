import pandas as pd

from io import StringIO
import re
import requests
import time


adult_ll_history = pd.read_csv('data/adult_ll_history.csv', parse_dates=True)
input_size = adult_ll_history.size

html_doc = requests.get('https://fabtcg.com/resources/rules-and-policy-center/living-legend/').text
date = re.search('as of ([^(]*)', html_doc).group(1).strip()

current_adult_ll_table = pd.read_html(StringIO(html_doc), match='(Classic Constructed|Adult Hero) Living Legend')[0][['Hero', 'Living Legend Points']]
current_adult_ll_table.fillna(value=0, inplace=True)
current_adult_ll_table.replace('-', 0, inplace=True)
current_adult_ll_table.rename(columns={'Living Legend Points': pd.to_datetime(date).strftime('%Y-%m-%d')}, inplace=True)
current_adult_ll_table.sort_values(by=['Hero'], inplace=True)


adult_ll_history = pd.concat([current_adult_ll_table.set_index('Hero'), adult_ll_history.set_index('Hero')], axis=1, join='outer').reset_index()
output_size = adult_ll_history.size

if input_size != output_size:
    adult_ll_history.to_csv("data/adult_ll_history.csv", index=False)
    print(date)