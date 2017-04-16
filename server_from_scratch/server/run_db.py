from sqlalchemy import create_engine
from models.meta import Base, Session
from models.tables import Partner, Terminal, Payment, Service, Encashment

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

# log.info("Creating tables")
engine = create_engine('sqlite:///preprocessing.db', echo=True)
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)
# log.info("Successfully setup")


def session_decorator(foo):
    def inner(*args, **kwargs):
        new_row = foo()
        session.add(new_row)
        session.commit()
        session.flush()

    return inner


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


# start()

def search_partners_transaction(session_, model, start_date, end_date):
    query_result = session_.query(model.partner_id, model.summ). \
        filter(model.date_time.between(start_date, end_date)). \
        filter(model.summ > 0).all()
    return query_result


def search_date(session, model, start_date, end_date):
    query_result = session.query(model.id, model.datetm).filter(model.datetm.between(start_date, end_date)).all()
    return query_result


def search(session_, model, partner_id):
    query_result = session_.query(model.title, model.comment).filter(model.partner_id == partner_id).all()
    return query_result


print(search(session, Partner, 111))
