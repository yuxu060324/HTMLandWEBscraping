import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_race_info(race_url, info):

    res = requests.get(race_url)
    race_soup = BeautifulSoup(res.content, 'html.parser')

    race_list = race_soup.find_all("tr", class_="HorseList")
    len(race_list)
    list = [ x for x in race_list[1].stripped_strings ]
    del list[2:10]

    horse_url = race_soup.find("a", title=list[2])

    print(list)
    print(horse_url["href"])

url = "https://race.netkeiba.com/race/shutuba.html?race_id=202109050611&rf=race_list"
table_unit_list = ["枠", "馬番", "馬名", "性齢", "斤量", "騎手", "厩舎名", "調教師", "オッズ", "人気"]
table_info = ["HorseInfo", "Barei Txt_C", "Txt_C", "Jockey", "Trainer", "Txt_R Popular", "Popular Popular_Ninki Txt_C"]

get_race_info(url, table_info)

# table = pd.read_html(url)[0]

