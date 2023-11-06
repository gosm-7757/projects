import requests
from bs4 import BeautifulSoup
import time
import urllib.request

# ユーザーが見るメニュー
def prtmenu(read_file) :
    print("1. 株確認    2. 株追加    3. 株の状況出力")
    choice = input("メニュー選択 => ")
    if choice == '1':
        check_stock(read_file)                      # ファイルの保存されている株の種類を持ってくるファンクション呼出
    elif choice == '2':
        add_stock(read_file)                        # 株を追加するファンクション呼出
    elif choice == '3':
        prt_stock_info(read_file)                  # 株データを出歴するファンクション呼出
    else:
        stop = input("終わりますか? [はい/いいえ] =>")      # 1, 2, 3 以外の入力の場合「終わりますか」を聞く
        if stop == 'はい':                                # 「肺の場合」stopをリターンする
            return 'stop'               
        elif stop != 'いいえ':
            print("無効入力")                    # 「はい、いいえ」ではないときに無視して繰り返す。
        
        

# １を選んだ時に飛び出されるファンクション
def check_stock(file_ob1):
    for i in file_ob1: # 一行ずつ出力
        item = i.strip().split(':') # 一行ずつ リストにして 「:」を 基準に項目を分ける。
        if len(item) != 2:
            continue
        stock_dict[item[0]] = item[1]
    for key, value in stock_dict.items() : 
        print(f"{key} : {value}")




# ２を選んだ時に飛び出されるファンクション
def add_stock(read_file):
    key = input("株の名前入力 => ")
    value = input("株のコードを入力 => ")
    with open('D:/python_web_crawling/learning_crawling/stock/stock_items.txt', 'a', encoding='UTF-8') as append_file:
        append_file.write(f'\n{key}:{value}')
    print("株入力完了")




# ３を選んだ時に飛び出されるファンクション
def prt_stock_info(file_ob3):
    stock_code = input('株のコードを入力してください。 => ')
                                
    # naverから株のデータを持ってくる
    naver_stock = requests.get(f'https://finance.naver.com/item/sise.naver?code={stock_code}')
    souped_stock = BeautifulSoup(naver_stock.content, 'html.parser')

    # 株のデータを持ってくる
    result['現在価格'] = souped_stock.find_all('strong', class_='tah')[0].text
    result['取引量'] = souped_stock.find_all('span', class_='tah')[5].text
    result['上限価格'] = souped_stock.select('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(8) > td:nth-child(2) > span')[0].text
    result['下限価格'] = souped_stock.select('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(9) > td:nth-child(2) > span')[0].text

    # 結果出力コード
    for key, value in result.items() :
        print(f"{key} : {value}")
    save = input("保存しますか? [はい/いいえ] => ")
    if save == 'はい':
        stock_name = input("株の名前入力 => ")
        img = souped_stock.select('#img_chart_area')[0]['src']
        save_result(stock_name, img, result)  # 保存するファンクション呼出
        print("保存しました。")
    elif save != 'いいえ':
        print("間違えた入力")
    
    

# 株の状況を保存するファンクション
def save_result(stock_name, img, result_ob) :
    with open('D:/python_web_crawling/learning_crawling/stock/save_stock_info.txt', 'a', encoding='UTF-8') as save_file:
        # チャートを保存するコード
        urllib.request.urlretrieve(img, f'D:/python_web_crawling/learning_crawling/stock/사진저장/{stock_name}.png')
        # 保存した時間
        tm = time.strftime("%Y年 %m月 %d日  %H : %M") 
        save_file.write("----------\n株名 : " + stock_name + "\n" + tm + "\n\n")
        for key, value in result_ob.items():
            save_file.write(f"{key} : {value}\n")
    
    



stock_dict = {} # 保存されている株を入れるディクショナリー
result = {}        # 現在状況を入れるディクショナリー


# 実行部分
with open('D:/python_web_crawling/learning_crawling/stock/stock_items.txt', 'r', encoding='UTF-8') as read_file :
    while True:
        stop = prtmenu(read_file) # ユーザーに見せるメニューのファンクション呼出
        if stop == "stop": # リターンの値が「stop」であれば繰り返し脱出
            # 開いてるファイルは閉めて脱出
            break



