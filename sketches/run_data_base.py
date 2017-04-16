import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, backref, relationship
from sqlalchemy.sql import select

from models.tables import Partner, Terminal, Payment, Service, Encashment
from models import Base

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
engine = create_engine('sqlite:///preprocessing.db', echo=True)
Session.configure(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def add_partner(session_, partner_id, title, comment=""):
    new_row = Partner(partner_id=partner_id, title=title, comment=comment)
    session_.add(new_row)
    session_.commit()


def add_service(session_, date_time, terminal_id, transaction_id, event_type):
    new_row = Service(date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id,
                      event_type=event_type)
    session_.add(new_row)
    session_.commit()


def add_payment(session_, date_time, terminal_id, transaction_id, partner_id, summ):
    new_row = Payment(date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id,
                      partner_id=partner_id,
                      summ=summ)
    session_.add(new_row)
    session_.commit()


def add_encashment(session_, date_time, terminal_id, transaction_id, accumulator_id, summ):
    new_row = Encashment(date_time=date_time, terminal_id=terminal_id, transaction_id=transaction_id,
                         accumulator_id=accumulator_id, summ=summ)
    session_.add(new_row)
    session_.commit()


def start():
    add_partner(session, partner_id=111, title="MTS", comment="Яйца")
    add_partner(session, partner_id=222, title="MegaFon", comment="NWGSM")
    add_partner(session, partner_id=333, title="Tele 2", comment="Шведы")
    add_partner(session, partner_id=444, title="Yota", comment="Поверх Мегафона")
    add_partner(session, partner_id=555, title="BeeLine", comment="Пчелайн")
