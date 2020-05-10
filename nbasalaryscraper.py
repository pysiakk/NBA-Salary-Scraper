from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def salary_scrape(year):
    src = "http://www.espn.com/nba/salaries/_/year/" + str(year) + "/page/"
    data = None
    for k in range(1, 20):
        url = src + str(k)
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
        rows = soup.findAll('tr')[1:]
        player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        stats = pd.DataFrame(player_stats, columns=[th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('td')])
        stats = stats[stats.RK != "RK"].reset_index(drop=True)
        for i, name in enumerate(stats.NAME):
            stats.NAME[i] = re.sub(",\s.*", "", name)
        for i, salary in enumerate(stats.SALARY):
            stats.SALARY[i] = int(re.sub("\$|,", "", salary))
        if k == 1:
            data = stats
        else:
            data = pd.concat([data, stats])
    return data.reset_index(drop=True)
