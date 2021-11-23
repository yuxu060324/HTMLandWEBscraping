from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import numpy as np
from itertools import combinations

ChromeDriver = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')

LINE_TOKEN = "B6pSW9uip417vO1qGi1IXzh9JINbrRJke8ovxA1BNxR"
LINE_API = "https://notify-api.line.me/api/notify"


def get_horse_DateFrame():

    horse_data = pd.DataFrame(columns=table_columns)
    int_columns = ["枠", "馬番", "年齢", "人気"]
    float_columns = ["斤量", "オッズ"]

    race_list = driver.find_elements(by=By.CLASS_NAME, value="HorseList")
    list_temp = [s.text for s in race_list]
    for i in range(len(list_temp)):
        list1 = list_temp[i].split(" ")
        list2 = list1[1].split("\n")
        list2[3:3] = list2[3][0], int(list2[3][1])
        del list1[1], list2[1], list2[4]
        list1[1:1] = list2

        if len(list1) == 11:
            del list1[8]

        horse_data.loc[i] = list1

    for index in int_columns:
        horse_data[index] = horse_data[index].astype(int)
    for index in float_columns:
        horse_data[index] = horse_data[index].astype(float)

    print(horse_data)

    return horse_data


def get_race_info():
    race_data_elements = driver.find_elements(by=By.CLASS_NAME, value='RaceData01')
    list_temp = [s.text for s in race_data_elements][0].split(" / ")
    race_data = [list_temp[1][0], list_temp[1][1:5], list_temp[1][8]]
    if len(list_temp[1]) >= 11:
        race_data.append(list_temp[1][10])
    if len(list_temp) >= 3:
        race_data.append(list_temp[2][-1])
        race_data.append(list_temp[3][-1])

    race_data_elements = driver.find_elements(by=By.CLASS_NAME, value='RaceData02')
    location = [s.text for s in race_data_elements][0].split(" ")[1]
    race_data.append(location)

    print(race_data)

    return race_data


def get_url_dictionary():
    url_dic = {}
    table = driver.find_element(by=By.TAG_NAME, value="tbody")
    horse_elements = table.find_elements(by=By.CLASS_NAME, value='HorseName')
    jockey_elements = table.find_elements(by=By.CLASS_NAME, value="Jockey")

    for i in range(len(horse_data)):
        horse_aTag = horse_elements[i].find_element(by=By.TAG_NAME, value='a')
        horse_url = horse_aTag.get_attribute("href")
        url_dic[horse_data.at[i, "馬名"]] = horse_url

        jockey_aTag = jockey_elements[i].find_element(by=By.TAG_NAME, value='a')
        jockey_url = jockey_aTag.get_attribute("href")
        url_dic[horse_data.at[i, "騎手"]] = jockey_url

    print(url_dic)

    return url_dic


def send_LINE_notify():

    race_name = driver.find_element(by=By.CLASS_NAME, value='RaceName').text

    row_index = np.arange(len(horse_data))
    odds_rank = horse_data.sort_values('オッズ')
    odds_rank.set_axis(row_index, axis=0, inplace=True)

    send_message = "\n\n"+race_name+"\n"\
                   + str(race_data[6])+str(race_data[1])+"m"

    send_message += "\n\n【オッズ昇順】\n"

    for i in range(len(odds_rank)):
        send_message += "【" + str(odds_rank["馬番"].loc[i]) + "】" \
                        + str(odds_rank["馬名"].loc[i]) + "(" \
                        + str(odds_rank["オッズ"].loc[i]) + "倍)\n"

    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    data = {'message': send_message}
    requests.post(LINE_API, headers=headers, data=data)


def replace_MLdata(horse_data):

    print(horse_data)

    MLdata = 0

    for i in range(len(horse_data)):
        if horse_data["性別"].loc[i] == "牡":  # オス
            horse_data["性別"].loc[i] = 1
        if horse_data["性別"].loc[i] == "牝":  # メス
            horse_data["性別"].loc[i] = 0

    return MLdata


base_race_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
race_id = "202109050611"  # "202105050812"
add_url = "&rf=shutuba_submenu"
race_card_url = base_race_url + race_id + add_url

table_columns = ["枠", "馬番", "馬名", "性別", "年齢", "斤量", "騎手", "厩舎", "オッズ", "人気"]

chrome_service = fs.Service(executable_path=ChromeDriver)
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.implicitly_wait(10)  # JavaScriptなどの読み込みを待機するプログラム
driver.get(race_card_url)

race_data = get_race_info()
horse_data = get_horse_DateFrame()
url_dic = get_url_dictionary()
MLdata = replace_MLdata(horse_data=horse_data)

send_LINE_notify()
