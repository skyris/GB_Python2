from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from models.meta import Base, Session
from models.tables import Partner, Terminal, Payment, Service, Encashment
import functools

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



def session_decorator(model, session=session):
    """ decorator = session_decorator(Partner)
        add_partner = decorator(add_partner)"""
    def decorator(func):
        @functools.wraps(func)
        def inner(**kwargs):
            new_row = model(**kwargs)
            session.add(new_row)
            session.commit()

        return inner

    return decorator


@session_decorator(Partner)
def add_partner(**kwargs):
    pass


@session_decorator(Terminal)
def add_terminal(**kwargs):
    pass


@session_decorator(Service)
def add_service(**kwargs):
    pass


@session_decorator(Payment)
def add_payment(**kwargs):
    pass


@session_decorator(Encashment)
def add_encashment(**kwargs):
    pass


# add_partner(dict(partner_id=123, title="Рост", comment="труба"))

"""
def insert_into_table(table, **kwargs):
    ins = getattr(table, "insert")
    insert = ins().values(**kwargs)
    conn = engine.connect()
    conn.execute(insert)
"""


def insert_into_table(session_, **kwargs):
    pass


def start():
    add_partner(partner_id=111, title="MTS", comment="Яйца")
    add_partner(partner_id=222, title="MegaFon", comment="NWGSM")
    add_partner(partner_id=333, title="Tele 2", comment="Шведы")
    add_partner(partner_id=444, title="Yota", comment="Поверх Мегафона")
    add_partner(partner_id=555, title="BeeLine", comment="Пчелайн")

#
# try:
#     start()
# except IntegrityError:
#     pass


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


def delete_row(session_, model, column, value):
    session_.query(model).filter(getattr(model, column) == value).delete()
    session_.commit()

# delete_row(session, Partner, "partner_id", 333)



# print(search(session, Partner, 111))
