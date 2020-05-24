from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def salary_scrape(year):
    src = "http://www.espn.com/nba/salaries/_/year/" + str(year+1) + "/page/"
    data = None
    for k in range(1, 20):
        url = src + str(k)
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
        rows = soup.findAll('tr')[1:]
        refs = [[j["href"] for j in rows[i].findAll('a')] for i in range(len(rows))]
        links = []
        for i in refs:
            if len(i) != 0:
                urlbirth = i[0]
                htmlbirth = urlopen(urlbirth)
                soupbirth = BeautifulSoup(htmlbirth, features="html.parser")
                birthdate = soupbirth.findAll('div', {"class": "fw-medium clr-black"})[0].getText()
                if birthdate[-1] == 's':
                    birthdate = soupbirth.findAll('div', {"class": "fw-medium clr-black"})[1].getText()[:-5]
                links.append(birthdate)
                
        player_stats = [[td.getText() for i, td in enumerate(rows[i].findAll('td'))] for i in range(len(rows))]
        stats = pd.DataFrame(player_stats, columns=[th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('td')])
        stats = stats[stats.RK != "RK"].reset_index(drop=True)
        stats = pd.concat([stats, pd.DataFrame(links, columns=["DOB"])], 1)
        for i, name in enumerate(stats.NAME):
            stats.NAME[i] = re.sub(",\s.*", "", name)
        for i, salary in enumerate(stats.SALARY):
            stats.SALARY[i] = int(re.sub("\$|,", "", salary))
        if k == 1:
            data = stats
        else:
            data = pd.concat([data, stats])
        
    return data.reset_index(drop=True)
