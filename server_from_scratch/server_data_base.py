import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, backref, relationship

Session = sessionmaker()
# engine = create_engine("sqlite:///:memory:", echo=True)
engine = create_engine('sqlite:///preprocessing.db', echo=True)
Session.configure(bind=engine)
session = Session()

Base = declarative_base()


class Partner(Base):
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(50))
    comment = Column(String(150))

    def __repr__(self):
        return "<Partner(id={} title={} comment={})" \
            .format(self.partner_id, self.title, self.comment)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer)
    transaction_id = Column(Integer)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), nullable=False)
    summ = Column(Integer)
    partner = relationship("Partner", backref=backref("payments", order_by=id))

    def __repr__(self):
        return "<Payment(id={} datetime={} partner_id={} summ={})" \
            .format(self.id, self.date_time, self.partner_id, self.summ)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer)
    transaction_id = Column(Integer)
    event_type = Column(String(50))

    def __repr__(self):
        return "<Service(id={} datetime={} terminal_id={} event_type={})" \
            .format(self.id, self.date_time, self.terminal_id, self.event_type)


class Encashment(Base):
    __tablename__ = "encashments"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer)
    transaction_id = Column(Integer)
    accumulator_id = Column(Integer)
    summ = Column(Integer)

    def __repr__(self):
        return "<Encashment(id={} datetime={} partner_id={} summ={})" \
            .format(self.id, self.date_time, self.accumulator_id, self.summ)


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
