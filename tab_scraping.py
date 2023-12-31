#TABのリンクから、自動的に保存する仕組み

from urllib.request import urlopen
import os
import time
import path as path
from bs4 import  BeautifulSoup
from pywebcopy import save_webpage

wanted_url=input("大会TABのHPのリンクを入力してください")
html=urlopen(wanted_url)
bs=BeautifulSoup(html.read(),"html.parser")
wanted=bs.find_all("a",{"class":"nav-link"})


namelist=["Main Page"]
urllist=[""]
for tag in wanted:
    name=tag.get_text()
    namespilt=list(name)
    #print(namespilt)
    url=tag.get("href")
    url_split=url.split("/")
    while namespilt[0]== "\n" or namespilt[0]==" ":
        del namespilt[0]
    while namespilt[-1]== "\n" or namespilt[-1]==" ":
        del namespilt[-1]

    name="".join(namespilt)
    namelist.append(name)

    #URL listに関する処理(URLの後半部分の構成)
    head=wanted_url.split("/")
    url_split=url.split("/")
    for x in head:
        if x in url_split:
            url_split.remove(x)
    url="/".join(url_split)
    urllist.append(url)
#print(namelist)
#print(urllist)
print(namelist,"\n\n")
#URLの全体構成
for i in range(len(urllist)):
    urllist[i]=wanted_url+urllist[i]
print(urllist)

#htmlファイルのままに保存する
route = "C:"
tour = input("大会名を入力してください") + str("TAB")
try:
    os.mkdir(os.path.join(route, tour))
    route = os.path.join(route, tour)
except FileExistsError:
    os.mkdir(os.path.join(route, tour, "NEW"))
    route = os.path.join(route, tour, "NEW")
for x, y in zip(namelist, urllist):
    try:
        kwargs = {'project_name': x}
        save_webpage(url=y, project_folder=os.path.join(route, x), **kwargs, open_in_browser=False)
        print(x, "が保存されました")
    except ConnectionError:
        print(x, "が保存されませんでした")
    finally:
        time.sleep(3)


#urllistからなるtxtファイルの作成
txt_route=os.path.join(route,f"{tour}.txt")
f=open(txt_route,"w")
for x in urllist:
    f.write(x)
    f.write("\n")
f.close()

#txtファイル内のサイトを、chormeを用いて、PDFとして保存する
txt_route=os.path.join(route,f"{tour}.txt")
f=open(txt_route,"w")
for x in urllist:
    f.write(x)
    f.write("\n")
f.close()


#PDF保存
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import json

# 保存対象URL一覧取得
urls = []
with open(txt_route, mode='rt', encoding='utf-8') as f:
    urls = f.readlines()

# Chrome の印刷機能でPDFとして保存
options = webdriver.ChromeOptions()
# PDF印刷設定
appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "pageSize": 'A4'
}
# ドライバへのPDF印刷設定の適用
options.add_experimental_option("prefs", {
    "printing.print_preview_sticky_settings.appState":
    json.dumps(appState),
    'savefile.default_directory':route,
    'savefile.prompt_for_download': True,
    'savefile.directory_upgrade': True,
    'safebrowsing.enabled': True
})
options.add_argument('--kiosk-printing')
with webdriver.Chrome("C:/chromedriver", options=options) as driver:
    # 任意のHTMLの要素が特定の状態になるまで待つ
    wait = WebDriverWait(driver, 15)
    for url in urls:
        driver.implicitly_wait(10)
        driver.get(url)
        # ページ上のすべての要素が読み込まれるまで待機
        wait.until(EC.presence_of_all_elements_located)
        # PDFとして印刷
        driver.execute_script("")
        driver.execute_script('window.print()')
        print("保存できました")
        # 待機
        time.sleep(10)
    driver.quit()
