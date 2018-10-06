# coding: utf-8

import os
import time

import selenium
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from joblib import Parallel, delayed

options = Options()
# Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
options.add_argument('--headless')

# ChromeのWebDriverオブジェクトを作成する。
driver = webdriver.Chrome(executable_path='/Users/kwatanabe/.local/bin/chromedriver', chrome_options=options)

driver.get('https://movies.yahoo.co.jp/movie/')

with open("hulu_movie_list.txt") as f:
    movie_lists = f.readlines()

out_fn = "movie_scores.tsv"
if os.path.exists(out_fn):
    os.remove(out_fn)

waitsec = 2

for movie in tqdm(movie_lists):
    movie = movie.replace(os.linesep, "")

    # 検索語を入力して送信する。
    input_element = driver.find_element_by_xpath('//*[@id="h_srch"]/div/form/input')
    input_element.send_keys(movie)

    try:
        input_element.send_keys(Keys.RETURN)
        time.sleep(waitsec)
    except selenium.common.exceptions.StaleElementReferenceException:
        print(movie + " has error....")
        continue

    try:
        # TODO li[1]が必ずしも意図するものとは限らない。
        next_url = driver.find_element_by_xpath('//*[@id="list-module"]/li[1]/a').click()
    except selenium.common.exceptions.NoSuchElementException:
        print(movie + " has error....")
        continue


    time.sleep(waitsec)

    sel = Selector(text=driver.page_source)
    score = sel.xpath('//*[@id="mv"]/div/div[2]/p[2]/span/span/text()').extract_first()  # OK

    if score is None:
        score = -1
        n_eval = -1

    else:
        n_eval = sel.xpath('//*[@id="mv"]/div/div[2]/p[2]/span/small[2]/text()').extract_first()
        n_eval = n_eval.split(":")[-1].replace("件", "").replace(",", "")  # OK

    with open(out_fn, "a") as f:
        f.write("%s\t%s\t%s" % (movie, score, n_eval) + os.linesep)

driver.quit()  # ブラウザーを終了する。
