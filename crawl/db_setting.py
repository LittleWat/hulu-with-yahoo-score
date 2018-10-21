import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DATABASE = os.environ.get('DATABASE_URL') or "postgresql://localhost/sample-db"

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=ENGINE)
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()
