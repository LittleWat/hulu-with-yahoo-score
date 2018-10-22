# coding: utf-8
import atexit
import os

import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template

from crawl.db_setting import Base
from crawl.db_setting import ENGINE
from crawl.db_setting import session
from crawl.items import Time
from crawl.selenium_hulu import HuluSelenium
from crawl.selenium_yahoo_movie import YahooMovieSelenium

app = Flask(__name__)

Base.metadata.create_all(bind=ENGINE, tables=[Time.__table__])


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


cron = BackgroundScheduler(daemon=True)
cron.add_job(func=crawling_job, trigger="cron", hour=7, minute=20)
# cron.add_job(func=crawling_job, trigger="interval", seconds=10)
cron.start()

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))


def add_footable_to_pandas_html(text):
    before_header = '<table border="1" class="dataframe">'
    after_header = '<table border="1" class="table table-striped" ' \
                   'data-paging="true" data-paging-size="50" data-paging-limit="5" ' \
                   'data-filtering="true" data-sorting="true">'
    return text.replace(before_header, after_header)


@app.route("/")
def show_tables():
    movie_df = pd.read_sql("SELECT title, score, n_eval FROM yahoo", ENGINE)
    movie_df = movie_df.sort_values("score", ascending=False)
    movie_df.index = np.arange(1, movie_df.shape[0] + 1)

    last_crawling_time_str = session.query(Time.time).order_by(Time.time.desc()).first()[0].strftime(
        '%Y-%m-%d %H:%M:%S')

    return render_template('view.html', table=add_footable_to_pandas_html(movie_df.to_html()),
                           last_crawling_time=last_crawling_time_str)


if __name__ == "__main__":
    port = os.environ.get("PORT", "5000")
    app.run(host="0.0.0.0", port=int(port), debug=True, use_reloader=False)
