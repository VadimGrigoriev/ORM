import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    def __str__(self):
        return self.name


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id", ondelete='CASCADE'), nullable=False)

    publisher = relationship('Publisher', backref="book")

    def __str__(self):
        return self.title


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id", ondelete='CASCADE'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id", ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.BigInteger, nullable=False)

    book = relationship('Book', backref="stock")
    shop = relationship('Shop', backref="stock")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id", ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.BigInteger, nullable=False)

    stock = relationship('Stock', backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

