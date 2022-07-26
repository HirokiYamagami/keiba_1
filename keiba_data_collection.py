
# coding: utf-8

# In[ ]:

#各年のレース情報取得

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import pandas
import os


#レース名を入力する(ディレクトリ名になる)
race_name="kikkasyo2022"

#ディレクトリ作成 (好きなディレクトリを指定)
keiba_dir =  "./競馬/{}".format(race_name)
os.makedirs(keiba_dir+"/raceInfo")
os.makedirs(keiba_dir+"/horseInfo")
os.makedirs(keiba_dir+"/allInfo")


#過去20年のレースIDの取得
raceid_list = []
#URLを変更することで有馬記念以外のレースも取得可能(OPレース等名前があるレースに限る)
#url = "https://db.netkeiba.com/?pid=race_list&word=%5E%CD%AD%C7%CF%B5%AD%C7%B0"
url = "https://db.netkeiba.com/?pid=race_list&word=%5E%B5%C6%B2%D6%BE%DE"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

soup_txt_race = soup.find_all(href = re.compile("/race/20"))

for num in range(20):
    raceid_list.append(soup_txt_race[num].attrs['href'])

#過去20年のレースのデータを取得
for count,i in enumerate(raceid_list):
    url = "https://db.netkeiba.com" + i
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    soup_span = soup.find_all("span")
    len(soup_span)

    #頭数
    allnum = int((len(soup_span) - 8) / 3)

    #馬の情報を以下で取得
    soup_txt_l = soup.find_all(class_ = "txt_l")

    #馬の名前
    name = []
    for num in range(allnum):
        name.append(soup_txt_l[4 * num].contents[1].contents[0])

    #騎手名
    jockey = []
    for num in range(allnum):
        jockey.append(soup_txt_l[4 * num + 1].contents[1].contents[0])

    #馬番
    soup_txt_r = soup.find_all(class_ = "txt_r")
    horse_number = []
    for num in range(allnum):
        horse_number.append(soup_txt_r[1 + 5 * num].contents[0])

    #走破タイム
    runtime = [] 
    for num in range(allnum):
        try:
            runtime.append(soup_txt_r[2 + num * 5].contents[0])
        except IndexError:
            runtime.append(None)

    #オッズ
    odds = []
    for num in range(allnum):
        try:
            odds.append(soup_txt_r[3 + 5 * num].contents[0])
        except IndexError:
            odds.append(None)

    #通過順
    soup_nowrap = soup.find_all("td",nowrap = "nowrap",class_ = None)
    pas = []
    for num in range(allnum):
        try:
            pas.append(soup_nowrap[3 * num].contents[0])
        except IndexError:
            pas.append(None)

    #体重
    weight = []
    for num in range(allnum):
        try:
            weight.append(soup_nowrap[3 * num + 1].contents[0])
        except IndexError:
            weight.append(None)

    #性齢
    soup_tet_c = soup.find_all("td",nowrap = "nowrap",class_  = "txt_c")
    sex_old = []
    for num in range(allnum):
        sex_old.append(soup_tet_c[6 * num].contents[0])

    #斤量
    handi = []
    for num in range(allnum):
        handi.append(soup_tet_c[6 * num + 1].contents[0])

    #上がり
    last = []
    for num in range(allnum):
        try:
            last.append(soup_tet_c[6 * num + 3].contents[0].contents[0])
        except IndexError:
            last.append(None)

    #人気
    pop = []
    for num in range(allnum):
        try:
            pop.append(soup_span[3 * num + 10].contents[0])
        except IndexError:
            pop.append(None)
    
    #データ格納
    houseInfo = [name,jockey,horse_number,runtime,odds,pas,weight,sex_old,handi,last,pop]
    
    #CSV書き出し
    #ファイルパス指定
    year = 2021-count    
    filepass1 = keiba_dir+"/raceInfo/{}_test.csv".format(year)
    with open(filepass1, 'a', newline = '',encoding = "SHIFT-JIS") as f:
        csv.writer(f).writerows(houseInfo)
    col_num = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    df = pandas.read_csv(filepass1,encoding = "SHIFT-JIS",names = col_num)
    
    #列名追加
    df_mod = df.rename(index = {0:"馬名",1:"騎手名",2:"枠順",3:"走破タイム",4:"オッズ",5:"通過順位",6:"馬体重",7:"性齢",8:"斤量",9:"上がり3ハロン",10:"人気"})
  
    #ファイル書き出し
    filepass2 = keiba_dir+"/raceInfo/{}.csv".format(year)
    df_mod.to_csv(filepass2)
    
    #testファイルの削除
    os.remove(filepass1)
    
    #間隔
    time.sleep(1)

#各年の出走馬のデータ取得

#関数定義
#列名から部分一致でindexを返す関数の定義
def inclusive_index(lst, purpose):
    for i, e in enumerate(lst):
        if purpose in e: return i

    raise IndexError

#レースidと検索用パラメータの格納
race_para_list=[]
raceid_list = []
for num in range(20):
    race_para_list.append(soup_txt_race[num])
    raceid_list.append(soup_txt_race[num].attrs['href'])

#過去20年のレースのデータを取得
for count,i in enumerate(raceid_list):
    raceurl = "https://db.netkeiba.com" + i
    r2 = requests.get(raceurl)
    soup2 = BeautifulSoup(r2.content, "html.parser")
    soup2_span = soup2.find_all("span")
    len(soup2_span)
    #出走頭数
    allnum = int((len(soup2_span) - 8) / 3)

    #出走馬のページURL取得
    soup2_txt_h = soup2.find_all(href = re.compile("/horse/"))
    #出走馬のURL
    horse_url_list = [] 
    for num in range(allnum):
        horse_url_list.append(soup2_txt_h[num].attrs['href'])
        
    #出走馬のデータ取得
    for horse_url in horse_url_list:
        horseurl = "https://db.netkeiba.com"+horse_url
        r3 = requests.get(horseurl)
        soup3 = BeautifulSoup(r3.content, "html.parser")

        # 直近3回の出走レース名の取得
        soup3_txt_race = soup3.find_all(href = re.compile("/race/20"))
        soup3_txt_race_str = [str(n) for n in soup3_txt_race]
        idx=soup3_txt_race_str.index(str(race_para_list[count]))
        recent_race=[soup3_txt_race[idx+1],soup3_txt_race[idx+2],soup3_txt_race[idx+3]]
        recent_race_str=[str(n) for n in recent_race] 

        recent_race_list = []
        for num2 in range(0,3):
            try:
                recent_race_list.append(recent_race[num2].contents[0])
            except IndexError:
                recent_race_list.append(None)

        #直近3回の出走レースの詳細情報の取得 
        soup3_td = soup3.find_all('td')
        soup3_td_str = [str(n) for n in soup3_td]

        recent_race_info = []
        for race in  recent_race_str:
            try:
                idx2=inclusive_index(soup3_td_str,race)
                recent_race_info.append(race)
                recent_race_info.append(soup3_td[idx2+5].text)
                #recent_race_info.append(soup3_td[idx2+6].text)
                recent_race_info.append(soup3_td[idx2+7].text)
            except IndexError:
                recent_race_info.append(None)
       #print(recent_race_info)
            
        #みんなの評価の取得
        soup_txt_review = soup3.find_all(src = re.compile("https://cdn.netkeiba.com/img.db//style/netkeiba.ja/image/review_bar_"))
        #芝適正(値が大きいほどダート適正)
        turf_type = soup_txt_review[1].get("width")
        #距離適性(値が大きいほど長距離適性)
        dist_type = soup_txt_review[3].get("width")
        #脚質(値が大きいほど追い込み)
        run_type = soup_txt_review[5].get("width")
        #成長(値が大きいほど晩成)
        grow_type = soup_txt_review[7].get("width")
        #馬場適性(値が大きいほど重馬場苦手)
        field_type = soup_txt_review[9].get("width")

        #馬の総合評価
        soup_stars = soup3.find_all(class_ = re.compile("star"))
        #総合評価
        try:
            soup_all_stars = soup_stars[0].contents[0].contents[0]
        except IndexError:
            soup_all_stars = ""

        #実績評価
        try:
            soup_result_stars = soup_stars[1].contents[0]
        except IndexError:
            soup_result_stars = ""
        #ポテンシャル評価
        try:
            soup_potential_stars = soup_stars[2].contents[0].contents[0]
        except IndexError:
            soup_potential_stars = ""
            
            
        #全ての結果を結合
        eachhorseInfo = [turf_type,dist_type,run_type,grow_type,field_type,soup_all_stars,soup_result_stars,soup_potential_stars]+recent_race_info
        #不正な文字コードを削除
        eachhorseInfo_mod = []
        for item in eachhorseInfo:
            item_mod = item.replace("\xa0","") 
            eachhorseInfo_mod.append(item_mod)
            
        #CSVに書き出し
        year = 2021-count
        filepass3 = keiba_dir+"/horseInfo/{}_test.csv".format(year)
        with open(filepass3, 'a',newline = '',encoding = "SHIFT-JIS") as f:
            csv.writer(f).writerow(eachhorseInfo_mod)
    
#csvの整理
    col_names=["芝適性","距離適性","脚質","成長","馬場適性","総合評価","実績評価","ポテンシャル評価","前走レース名","前走オッズ","前走成績","2走前レース名","2走前オッズ","2走前成績","3走前レース名","3走前オッズ","3走前成績"]
    df = pandas.read_csv(filepass3,encoding = "SHIFT-JIS",names=col_names)
    year = 2021-count
    filepass4 =  keiba_dir+"/horseInfo/{}.csv".format(year)
    #転置
    df.T.to_csv(filepass4)
    #testファイルの削除
    os.remove(filepass3)
    

#レースデータと出走馬のデータの結合

for year in range(2002,2022):
    racepass =  keiba_dir+"/raceInfo/" + str(year) + ".csv"
    horsepass =  keiba_dir+"/horseInfo/" + str(year) + ".csv"
    df1 = pandas.read_csv(racepass)
    df2 = pandas.read_csv(horsepass)
    df_concat = pandas.concat([df1,df2], axis = 0, ignore_index = False)
    allInfopass =  keiba_dir+"/allInfo/{}.csv".format(year)
    df_concat.to_csv(allInfopass, index = False)

# テスト
pandas.read_csv(keiba_dir+"/allInfo/2020.csv",index_col=0,encoding = "utf-8")


# In[401]:

#各年のレース情報取得

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import pandas
import os


#レース名を入力する(ディレクトリ名になる)
race_name="kikkasyo2022"

#ディレクトリ作成 (好きなディレクトリを指定)
keiba_dir =  "./競馬/{}".format(race_name)

# テスト
pandas.read_csv(keiba_dir+"/allInfo/2021.csv",index_col=0,encoding = "utf-8")


# In[ ]:



