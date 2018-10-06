# coding: utf-8
import os
import time

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HuluSelenium:
    TARGET_URL = 'https://www.happyon.jp/tiles/1039'  # 洋画
    _driver = None
    title_list = []
    _i = 1

    def __init__(self):
        def create_options():
            options = Options()
            # Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
            options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
            options.add_argument('--headless')

        options = create_options()

        # ChromeのWebDriverオブジェクトを作成する。
        self._driver = webdriver.Chrome(executable_path='/Users/kwatanabe/.local/bin/chromedriver',
                                        chrome_options=options)
        self._driver.get(self.TARGET_URL)
        self._driver.find_element_by_xpath('//*[@id="vod-vid-b-4"]/body/div[2]/main/div[2]/div/div/ul/li[1]').click()
        time.sleep(1)  # Chromeの場合はAjaxで遷移するので、とりあえず適当に2秒待つ。

    def _scroll(self, wait_sec=5):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_sec)

    def _get_title(self):
        def get_xpath():
            return '//*[@id="vod-vid-b-4"]/body/div[2]/main/div[3]/div[1]/div[%d]/a/@data-tracking-panel-title' % self._i

        sel = Selector(text=self._driver.page_source)
        return sel.xpath(get_xpath()).extract_first()

    def _save_title_list(self, out_filename="hulu_movie_list.tsv"):
        end_of_line = os.linesep
        str_ = end_of_line.join(self.title_list)

        with open(out_filename, 'wt') as f:
            f.write(str_)

        print("*** Finished saving! ***")

    def run(self):
        while True:
            title = self._get_title()
            if title is None:
                self._scroll()
                title = self._get_title()
                if title is None:
                    self._scroll()
                    title = self._get_title()
                    if title is None:
                        break

            print(title)

            self.title_list.append(title)
            self._i += 1

        self._driver.quit()  # ブラウザーを終了する。
        print("*** Finished running! ***")

        self._save_title_list()


if __name__ == '__main__':
    hulu_sele = HuluSelenium()
    hulu_sele.run()
