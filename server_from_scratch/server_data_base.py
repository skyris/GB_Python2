import datetime
import operator as op
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, backref, relationship
from sqlalchemy.sql import select, and_, or_, not_

"""
 2.а. Реализовать возможность создания структуры БД
    2.б. Реализовать возможность добавлять данные в БД (INSERT)
    2.в. Реализовать возможность удалять данные из БД (DELETE) ?????
    2.г. Реализовать возможность производить выборку данных (SELECT):
    * Выбрать платёжные транкции для указанного терминала (id) за указанный период (datetime).
    * За указанный период (datetime) по данным платёжных транзакций сформировать выборку какая сумма должна быть
            перечислена каждой фирме-партнёру (можно не учитывать тех партнёров, для которых нет платежей).
    * По данным платёжных транзакций сформировать выборку с указанием, какая сумма прошла через каждый терминал
            за указанный период.
    * *Дополнительно.* По каждому терминалу сформировать отчет, где отражаются временные периоды в течение дня
            (0-6, 6-12, 12-18, 18-24) и количество транзакций в каждый временной период.
"""
Session = sessionmaker()
engine = create_engine('sqlite:///new_preprocessing.db', echo=True)
Session.configure(bind=engine)
session = Session()

Base = declarative_base()
metadata = MetaData()

partners = Table("partners", metadata,
                 Column("partner_id", Integer, primary_key=True, unique=True),
                 Column("title", String(50)),
                 Column("comment", String(150))
                 )

payments = Table("payments", metadata,
                 Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
                 Column("date_time", DateTime),
                 Column("terminal_id", Integer),
                 Column("transaction_id", Integer),
                 Column("partner_id", Integer, ForeignKey(partners.columns.partner_id), nullable=False),
                 Column("summ", Integer)
                 # partner = relationship("Partner", backref=backref("payments", order_by=id))
                 )

services = Table("services", metadata,
                 Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
                 Column("date_time", DateTime),
                 Column("terminal_id", Integer),
                 Column("transaction_id", Integer),
                 Column("event_type", String(50))
                 )

encashments = Table("encashments", metadata,
                    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
                    Column("date_time", DateTime),
                    Column("terminal_id", Integer),
                    Column("transaction_id", Integer),
                    Column("accumulator_id", Integer),
                    Column("summ", Integer)
                    )

metadata.create_all(engine)

"""
"partners, partner_id=partner_id, title=title, comment=comment"

"services, date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id, event_type=event_type"

"payments, date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id, partner_id=partner_id, summ=summ"

"encashment, date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id, accumulator_id=accumulator_id, summ=summ"
"""


def fill_partners_table():
    conn = engine.connect()
    conn.execute(partners.insert(), [
        dict(partner_id=111, title="MTS", comment="Яйца"),
        dict(partner_id=222, title="MegaFon", comment="NWGSM"),
        dict(partner_id=333, title="Tele 2", comment="Шведы"),
        dict(partner_id=444, title="Yota", comment="Поверх Мегафона"),
        dict(partner_id=555, title="BeeLine", comment="Пчелайн"),
        dict(partner_id=777, title="KievStar", comment="Украинцы"),
    ])
    insert_into_table(partners, partner_id=888, title="VimpelCom", comment="Билайн")


def insert_into_table(table, **kwargs):
    ins = getattr(table, "insert")
    insert = ins().values(**kwargs)
    conn = engine.connect()
    conn.execute(insert)


def delete_eq(table, column, value):
    del_ = getattr(table, "delete")
    col = getattr(getattr(table, "c"), column)
    conn = engine.connect()
    conn.execute(del_().where(col == value))


def select_eq(table, column, value):
    col = getattr(getattr(table, "c"), column)
    s = select([table]).where(col < value)
    conn = engine.connect()
    return conn.execute(s)


def select_date_period(id, start_date, end_date):
    col = payments.c.id
    s = select([payments]).where(and_(col == id, payments.c.date_time.between(start_date, end_date)))
    conn = engine.connect()
    return conn.execute(s)

if __name__ == "__main__":
    pass
    # fill_partners_table()

    # delete_eq(partners, "partner_id", 777)

    # for row in select_eq(partners, "partner_id", 555):
    #     print(row)
    for row in select_date_period(1, datetime.datetime.now(), datetime.datetime.now()):
        print(row)