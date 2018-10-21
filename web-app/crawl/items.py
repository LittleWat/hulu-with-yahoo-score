import sys

from sqlalchemy import Column, Integer, String, Float

from db_setting import Base
from db_setting import ENGINE


class Hulu(Base):
    """
    Hulu data object
    """
    __tablename__ = 'hulu'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(200))
    url = Column('url', String(200))

    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

    def __repr__(self):
        return '<Title %r>' % self.title


class YahooMovie(Base):
    """
    YahooMovie data object
    """
    __tablename__ = 'yahoo'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(200))
    score = Column("score", Float)
    n_eval = Column("n_eval", Integer)

    def __init__(self, id, title, score, n_eval):
        self.id = id
        self.title = title
        self.score = score
        self.n_eval = n_eval

    def __repr__(self):
        return '<Title %r>' % self.title


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)


if __name__ == "__main__":
    main(sys.argv)
