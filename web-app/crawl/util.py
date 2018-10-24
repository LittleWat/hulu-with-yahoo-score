# coding: utf-8


def create_driver():
    import platform
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver

    options = Options()

    # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # エラーの許容
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')

    # headlessでは不要そうな機能
    options.add_argument('--disable-desktop-notifications')
    options.add_argument("--disable-extensions")

    # 言語
    options.add_argument('--lang=ja')

    # for local mac
    if platform.system() == "Darwin":
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        # ChromeのWebDriverオブジェクトを作成する。
        return webdriver.Chrome(executable_path='/Users/kwatanabe/.local/bin/chromedriver', chrome_options=options)

    # for heroku
    options.binary_location = "/app/.apt/usr/bin/google-chrome"
    return webdriver.Chrome(chrome_options=options)
