import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from crawl.db_setting import session
from crawl.items import Time
from crawl.selenium_hulu import HuluSelenium
from crawl.selenium_yahoo_movie import YahooMovieSelenium


def crawling_job():
    print("------ Hulu Crawling Started! ------")
    hulu_sele = HuluSelenium()
    hulu_sele.run()
    print("------ Hulu Crawling Finished! ------")

    print("------ Yahoo-movie Crawling Started! ------")
    ym_sele = YahooMovieSelenium()
    ym_sele.run()
    print("------ Yahoo-movie Crawling Finished! ------")

    # 最後にクローリングした時刻をDBに書き出す
    time = Time()
    session.add(time)
    session.commit()


def register_crawling_job_to_aspscheduler():
    cron = BackgroundScheduler(daemon=True)
    cron.add_job(func=crawling_job, trigger="cron", hour=3, minute=0)
    # cron.add_job(func=crawling_job, trigger="interval", seconds=10)
    cron.start()

    # Shutdown your cron thread if the web process is stopped
    atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == "__main__":
    crawling_job()
