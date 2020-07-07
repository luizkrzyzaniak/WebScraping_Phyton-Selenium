import requests, json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


url = 'https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1'
rankingTop10 = {}

rankDict = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}

def rank(type):

    field = rankDict[type]['field']
    label = rankDict[type]['label']

    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    htmlContent = element.get_attribute('outerHTML')

    soup = BeautifulSoup(htmlContent, 'html.parser')
    table = soup.find(name='table')

    df_Full = pd.read_html( str(table))[0].head(10) #.head está limitando até 10 de conteudo

    df = df_Full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']


    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
driver.implicitly_wait(10)

for i in rankDict:
    rankingTop10[i] = rank(i)

driver.quit()

with open('ranking.json', 'w', encoding='utf-8') as jsonFile:
    js = json.dumps(rankingTop10['points'], indent=4)
    jsonFile.write(js)