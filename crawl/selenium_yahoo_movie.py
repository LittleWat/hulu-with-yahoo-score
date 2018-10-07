# coding: utf-8

import os
import time

import selenium
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


class YahooMovieSelenium:
    _in_fn = "hulu_movie_list.txt"
    _out_fn = "movie_scores.tsv"

    _driver = None
    _title_list = []
    _waitsec = 2

    def __init__(self):
        def create_options():
            opt = Options()
            # Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
            opt.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
            opt.add_argument('--headless')
            return opt

        options = create_options()

        # ChromeのWebDriverオブジェクトを作成する。
        self._driver = webdriver.Chrome(executable_path='/Users/kwatanabe/.local/bin/chromedriver',
                                        chrome_options=options)

        self._driver.get('https://movies.yahoo.co.jp/movie/')

        with open(self._in_fn) as f:
            self._title_list = f.readlines()

        if os.path.exists(self._out_fn):
            os.remove(self._out_fn)

    def run(self):
        for movie in tqdm(self._title_list):
            movie = movie.replace(os.linesep, "")

            # 検索語を入力して送信する。
            input_element = self._driver.find_element_by_xpath('//*[@id="h_srch"]/div/form/input')
            input_element.send_keys(movie)

            try:
                input_element.send_keys(Keys.RETURN)
                time.sleep(self._waitsec)
            except selenium.common.exceptions.StaleElementReferenceException:
                print(movie + " has error....")
                continue

            try:
                # TODO li[1]が必ずしも意図するものとは限らない。
                next_url = self._driver.find_element_by_xpath('//*[@id="list-module"]/li[1]/a').click()
            except selenium.common.exceptions.NoSuchElementException:
                print(movie + " has error....")
                continue

            time.sleep(self._waitsec)

            sel = Selector(text=self._driver.page_source)
            score = sel.xpath('//*[@id="mv"]/div/div[2]/p[2]/span/span/text()').extract_first()  # OK

            if score is None:
                score = -1
                n_eval = -1

            else:
                n_eval = sel.xpath('//*[@id="mv"]/div/div[2]/p[2]/span/small[2]/text()').extract_first()
                n_eval = n_eval.split(":")[-1].replace("件", "").replace(",", "")  # OK

            with open(self._out_fn, "a") as f:
                f.write("%s\t%s\t%s" % (movie, score, n_eval) + os.linesep)

        self._driver.quit()  # ブラウザーを終了する。


if __name__ == '__main__':
    ym_sele = YahooMovieSelenium()
    ym_sele.run()
