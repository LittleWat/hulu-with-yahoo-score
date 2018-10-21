# coding: utf-8
import atexit
import datetime
import os
import subprocess

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from crawl.db_setting import ENGINE

app = Flask(__name__)

last_crawling_time_filename = "./data/last_crawling_time.txt"


def crawling_job():
    print("------ Hulu Crawling Started! ------")
    subprocess.check_call("python ./crawl/selenium_hulu.py", shell=True)
    print("------ Hulu Crawling Finished! ------")

    print("------ Yahoo-movie Crawling Started! ------")
    subprocess.check_call("python ./crawl/selenium_yahoo_movie.py", shell=True)
    print("------ Yahoo-movie Crawling Finished! ------")

    # 最後にクローリングした時刻をファイルに書き出す
    with open(last_crawling_time_filename, mode="w") as f:
        now = datetime.datetime.now()
        f.write(now.strftime("%Y-%m-%d %H:%M:%S"))


cron = BackgroundScheduler(daemon=True)
cron.add_job(func=crawling_job, trigger="cron", hour=22, minute=30)
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
    movie_df.index += 1

    with open(last_crawling_time_filename) as f:
        last_crawling_time_str = f.read()

    return render_template('view.html', table=add_footable_to_pandas_html(movie_df.to_html()),
                           last_crawling_time=last_crawling_time_str)


if __name__ == "__main__":
    port = os.environ.get("PORT", "5000")
    app.run(host="0.0.0.0", port=int(port), debug=True, use_reloader=False)
