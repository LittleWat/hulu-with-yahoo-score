import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def show_tables():
    movie_df = pd.read_csv("../crawl/movie_scores.tsv", sep="\t", names=["タイトル", "点数", "評価数"], index_col=0)
    movie_df = movie_df.sort_values("点数", ascending=False)
    movie_df.reset_index(inplace=True)
    return render_template('view.html', table=movie_df.to_html())


if __name__ == "__main__":
    app.run(debug=True)
