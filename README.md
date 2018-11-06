# hulu-with-yahoo-score

Hulu配信作品をYahoo映画のスコアでランク付けしたサイトをherokuで生成

- このコードが生成したサイト
   - https://hulu-with-yahoo-score.herokuapp.com
- qiitaの記事
   - https://qiita.com/LittleWat/items/7615923a2cfbb3a7fcef


## 設定
Python 3.6を使用
```
pip install -r requirements.txt 
```

## 参考記事
* [simple tables in a web app using flask and pandas with Python](https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html)
* [tableのソート、フィルタ、ページング、編集ができるjQueryプラグイン「footable.js」を使ってみた感想](http://chinpui.net/?p=6)
* [footable.jsのバグ](https://github.com/fooplugins/FooTable/issues/687)
    * footable.jsをこの通りに多少書き直した。
* [herokuでのスケジュール管理にAPSchedulerを使ってみる](http://www.stockdog.work/entry/2017/04/10/003452)
* [Chrome headless + seleniumをherokuで定期実行](http://katsulog.tech/regularly-run-chrome-headless-selenium-with-heroku/)
* [herokuのタイムゾーンを変更したらAPSchedulerが動いた話](http://www.stockdog.work/entry/2017/04/15/020130)
* [herokuでファイルが出力されない](https://stackoverflow.com/questions/39813677/writing-file-in-heroku-filesystem-and-reading-it-with-web-app)
* [【Heroku Postgresql】アドオンを追加し、テーブル操作を行う](https://www.shookuro.com/entry/2018/03/11/160201)
* [heroku で DB(postgresql)を利用するときのメモ](https://qiita.com/croquette0212/items/9b4dc5377e7d6f292671)
