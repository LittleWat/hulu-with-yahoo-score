# coding: utf-8

import os
from enum import IntEnum

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from util import create_driver


class SearchResultException(IntEnum):
    NO_SEARCH_RESULT = -1
    NO_EVALUATION = -2


class YahooMovieSelenium:
    _in_fn = os.path.join("data", "hulu_movie_list.txt")
    _out_fn = os.path.join("data", "movie_scores.tsv.tmp")
    _base_url = 'https://movies.yahoo.co.jp/movie/'

    _driver = None
    _wait = None
    _title_list = []

    def __init__(self):
        self._driver = create_driver()
        self._driver.get(self._base_url)
        self._wait = WebDriverWait(self._driver, 1)

        # 映画一覧の読み込み
        with open(self._in_fn) as f:
            self._title_list = f.readlines()

        if os.path.exists(self._out_fn):
            os.remove(self._out_fn)

    def _get_result_per_movie(self, movie):
        # 検索語を入力して送信する。

        input_xpath = '//*[@id="h_srch"]/div/form/input'

        input_element = self._driver.find_element_by_xpath(input_xpath)
        input_element.send_keys(movie)
        input_element.send_keys(Keys.RETURN)

        show_results_existing_xpath = "//div[@id='rsltmv']/div[@class='row' and 1]/div[@class='list-controller align-center' and 1]/span[@class='label' and 1]"

        try:
            self._wait.until(EC.presence_of_element_located((By.XPATH, show_results_existing_xpath)))

        # 検索結果がない場合
        except TimeoutException:
            return [int(SearchResultException.NO_SEARCH_RESULT)] * 2

        # TODO: li[1] (= 結果一覧のうち、最初の結果)を指定しているがこれが必ずしも意図するものとは限らない
        self._driver.find_element_by_xpath('//*[@id="list-module"]/li[1]/a').click()

        score_xpath = "//p[@class='mov_ave_star text-xlarge text-large--media-small']/span[@class='rating-score' and 1]/span[1]"
        n_eval_xpath = "//small[@class='text-xsmall']"

        try:
            score_element = self._wait.until(EC.presence_of_element_located((By.XPATH, score_xpath)))
            score = score_element.text

            n_eval_element = self._wait.until(EC.presence_of_element_located((By.XPATH, n_eval_xpath)))
            n_eval = n_eval_element.text.split(":")[-1].replace("件", "").replace(",", "")

            return score, n_eval

        # 未評価の場合
        except TimeoutException:
            return [int(SearchResultException.NO_EVALUATION)] * 2

    def run(self):
        # for movie in tqdm(self._title_list):
        for movie in self._title_list:
            movie = movie.replace(os.linesep, "")

            score, n_eval = self._get_result_per_movie(movie)

            print(movie, score, n_eval)
            with open(self._out_fn, "a") as f:
                f.write("%s\t%s\t%s" % (movie, score, n_eval) + os.linesep)

        self._driver.quit()  # ブラウザーを終了する。
        print("*** Finished running! ***")


if __name__ == '__main__':
    ym_sele = YahooMovieSelenium()
    ym_sele.run()
