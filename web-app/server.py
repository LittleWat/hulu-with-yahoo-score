import os

import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


def add_footable_to_pandas_html(text):
    before_header = '<table border="1" class="dataframe">'
    after_header = '<table border="1" class="table table-striped" ' \
                   'data-paging="true" data-paging-size="50" data-paging-limit="5" ' \
                   'data-filtering="true" data-sorting="true">'
    return text.replace(before_header, after_header)


@app.route("/")
def show_tables():
    movie_df = pd.read_csv("../crawl/movie_scores.tsv", sep="\t", names=["タイトル", "点数", "評価数"], index_col=0)
    movie_df = movie_df.sort_values("点数", ascending=False)
    movie_df.reset_index(inplace=True)
    movie_df.index += 1
    return render_template('view.html', table=add_footable_to_pandas_html(movie_df.to_html()))


if __name__ == "__main__":
    port = os.environ.get("PORT", "5000")
    app.run(host="0.0.0.0", port=int(port), debug=True)
