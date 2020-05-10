# NBA-Salary-Scraper
This repo contains a script for scraping NBA players' salaries from ESPN page.

## Usage

`
salary_scrape(year)
`

## Ouput

`Pandas.DataFrame` containing a position in the salary ranking, the name of a player, the team of a player and his salary in dollars.


## Examples

```python
l = salary_scrape(2020)
print(sal.iloc[0])
```

```python
RK                            1
NAME              Stephen Curry
TEAM      Golden State Warriors
SALARY                 40231758
Name: 0, dtype: object
```

