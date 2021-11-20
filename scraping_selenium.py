from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
import pandas as pd

ChromeDriver = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')

def get_horse_DateFrame():

    horse_data = pd.DataFrame(columns=table_columns)

    race_list = driver.find_elements(by=By.CLASS_NAME, value="HorseList")
    list_temp = [s.text for s in race_list]
    for i in range(len(list_temp)):
        list1 = list_temp[i].split(" ")
        list2 = list1[1].split("\n")
        del list1[1], list2[1]
        list1[1:1] = list2
        horse_data.loc[i] = list1

    print(horse_data)

    return horse_data

def get_race_info():

    race_data_elements = driver.find_elements(by=By.CLASS_NAME, value='RaceData01')
    list_temp = [s.text for s in race_data_elements][0].split(" / ")
    race_data = [list_temp[1][0], list_temp[1][1:5], list_temp[1][8], list_temp[1][10], list_temp[2][-1], list_temp[3][-1]]

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


base_race_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
race_id = "202109050611"
add_url = "&rf=shutuba_submenu"
race_card_url = base_race_url + race_id + add_url
table_columns = ["枠", "馬番", "馬名", "性齢", "斤量", "騎手", "厩舎", "オッズ", "人気"]

chrome_service = fs.Service(executable_path=ChromeDriver)
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.implicitly_wait(10) #JavaScriptなどの読み込みを待機するプログラム
driver.get(race_card_url)

horse_data = get_horse_DateFrame()
race_data = get_race_info()
url_dic = get_url_dictionary()

