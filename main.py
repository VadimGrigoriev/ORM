import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables
from sqlalchemy import or_
import json


def create_engine(sql="postgresql", login="postgres", password="159632", database="netology_data"):
    engine = sq.create_engine(f"{sql}://{login}:{password}@localhost:5432/{database}")
    return engine


def fill_table(session):
    """Функция заполняю БД данными"""
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_info(session, publisher_id=None, publisher_name=None):
    """Функция выводит информацию о книге"""
    q = session.query(Publisher).join(Book).join(Stock).join(Shop).join(Sale).filter(
        or_(Publisher.id == publisher_id, Publisher.name == publisher_name))
    for pub in q.all():
        for bo in pub.book:
            for st in bo.stock:
                for sa in st.sale:
                    print(f'{bo.title}  |  {get_nameshop(session, st.id_shop)}  |  {sa.price}  |  {sa.date_sale}')


def get_nameshop(session, id):
    """Функция возвращает название магазина по идентификатору"""
    q = session.query(Shop).filter(Shop.id == id).all()
    for n in q:
        return n


if __name__ == '__main__':
    create_tables(engine=create_engine())

    Session = sessionmaker(bind=create_engine())
    session = Session()

    fill_table(session)

    get_info(session, publisher_id=1)
