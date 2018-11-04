# coding: utf-8
import os

import numpy as np
import pandas as pd
from flask import Flask, render_template

from crawl.db_setting import Base
from crawl.db_setting import ENGINE
from crawl.db_setting import session
from crawl.items import Time
from movie_crawler import register_crawling_job_to_aspscheduler

app = Flask(__name__)

Base.metadata.create_all(bind=ENGINE, tables=[Time.__table__])


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

    try:
        last_crawling_time_str = session.query(Time.time).order_by(Time.time.desc()).first()[0].strftime(
            '%Y-%m-%d %H:%M:%S')
    except TypeError:
        last_crawling_time_str = "not finished yet..."

    return render_template('view.html', table=add_footable_to_pandas_html(movie_df.to_html()),
                           last_crawling_time=last_crawling_time_str)


if __name__ == "__main__":
    register_crawling_job_to_aspscheduler()

    port = os.environ.get("PORT", "5000")
    app.run(host="0.0.0.0", port=int(port), debug=True, use_reloader=False)
