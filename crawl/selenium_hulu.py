# coding: utf-8
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HuluSelenium:
    TARGET_URL = 'https://www.happyon.jp/tiles/1039'  # 洋画
    _out_fn = "hulu_movie_list.txt"

    _driver = None
    _title_list = []
    _i = 1

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
        self._driver.get(self.TARGET_URL)
        self._driver.find_element_by_xpath('//*[@id="vod-vid-b-4"]/body/div[2]/main/div[2]/div/div/ul/li[1]').click()

    def _scroll(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _get_title(self):

        def get_title_xpath():
            return "/html[@id='vod-vid-b-4']/body/div[@class='vod-frm--user01']/main[@class='vod-frm__main']/div[@class='vod-mod-content']/div[@class='vod-mod-tile']/div[@class='vod-mod-tile__item vod-utl-panel-opener'][%d]/a" % self._i

        try:
            wait = WebDriverWait(self._driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, get_title_xpath())))
            return element.text

        except TimeoutException:
            return None

    def run(self):
        while True:
            self._scroll()
            title = self._get_title()
            if title is None:
                break

            print(title)

            self._title_list.append(title)
            self._i += 1

            with open(self._out_fn, "a") as f:
                f.write(title + os.linesep)

        self._driver.quit()  # ブラウザーを終了する。
        print("*** Finished running! ***")


if __name__ == '__main__':
    hulu_sele = HuluSelenium()
    hulu_sele.run()
