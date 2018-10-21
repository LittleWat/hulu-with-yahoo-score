# coding: utf-8

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .db_setting import Base
from .db_setting import ENGINE
from .db_setting import session
from .items import Hulu
from .util import create_driver


class HuluSelenium:
    TARGET_URL = 'https://www.happyon.jp/tiles/1039'  # 洋画

    _driver = None
    _title_list = []
    _i = 1

    def __init__(self):
        self._driver = create_driver()
        self._driver.get(self.TARGET_URL)
        self._driver.find_element_by_xpath('//*[@id="vod-vid-b-4"]/body/div[2]/main/div[2]/div/div/ul/li[1]').click()

    def _scroll(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _get_data(self):

        def get_title_xpath():
            return "/html[@id='vod-vid-b-4']/body/div[@class='vod-frm--user01']/main[@class='vod-frm__main']/div[@class='vod-mod-content']/div[@class='vod-mod-tile']/div[@class='vod-mod-tile__item vod-utl-panel-opener'][%d]/a" % self._i

        def get_url_xpath():
            # FIXME: 正しいXPATH
            return '//*[@id="vod-vid-b-4"]/body/div[2]/main/div[3]/div[1]/div[%d]/a' % self._i
            # return '//*[@id="vod-vid-b-4"]/body/div[2]/main/div[3]/div[1]/div[%d]/a/@href' % self._i

        try:
            wait = WebDriverWait(self._driver, 10)
            title_element = wait.until(EC.element_to_be_clickable((By.XPATH, get_title_xpath())))
            url_element = wait.until(EC.element_to_be_clickable((By.XPATH, get_url_xpath())))
            return title_element.text, url_element.text

        except TimeoutException:
            return None, None

    def run(self):

        Hulu.__table__.drop(ENGINE, checkfirst=True)
        Base.metadata.create_all(bind=ENGINE, tables=[Hulu.__table__])

        while True:
            self._scroll()
            title, url = self._get_data()
            if title is None:
                break

            print(title)

            # 「10/31まで」といった余計な情報を削除
            if '\n' in title:
                title = title[title.find('\n') + 1:]

            self._title_list.append(title)

            hulu = Hulu(id=self._i, title=title, url=url)
            session.add(hulu)
            session.commit()

            self._i += 1

        self._driver.quit()  # ブラウザーを終了する。
        print("*** Finished running! ***")


if __name__ == '__main__':
    hulu_sele = HuluSelenium()
    hulu_sele.run()
