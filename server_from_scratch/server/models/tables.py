from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from models.meta import Base


class Partner(Base):
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(50))
    comment = Column(String(150))

    def __repr__(self):
        return "<Partner(id={} title={} comment={})" \
            .format(self.partner_id, self.title, self.comment)


class Terminal(Base):
    __tablename__ = "terminals"

    terminal_id = Column("terminal_id", Integer, primary_key=True, unique=True)
    title = Column("title", String(50))
    comment = Column("comment", String(150))
    pub_key = Column("pub_key", String(300))

    def __repr__(self):
        return "<Terminal(terminal_id={} title={} comment={})" \
            .format(self.terminal_id, self.title, self.comment)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer, ForeignKey("terminals.terminal_id"), nullable=False)
    transaction_id = Column(Integer)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), nullable=False)
    summ = Column(Integer)

    def __repr__(self):
        return "<Payment(id={} datetime={} partner_id={} summ={})" \
            .format(self.id, self.date_time, self.partner_id, self.summ)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer, ForeignKey("terminals.terminal_id"), nullable=False)
    transaction_id = Column(Integer)
    event_type = Column(String(50))

    def __repr__(self):
        return "<Service(id={} datetime={} terminal_id={} event_type={})" \
            .format(self.id, self.date_time, self.terminal_id, self.event_type)


class Encashment(Base):
    __tablename__ = "encashments"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_time = Column(DateTime)
    terminal_id = Column(Integer, ForeignKey("terminals.terminal_id"), nullable=False)
    transaction_id = Column(Integer)
    accumulator_id = Column(Integer)
    summ = Column(Integer)

    def __repr__(self):
        return "<Encashment(id={} datetime={} partner_id={} summ={})" \
            .format(self.id, self.date_time, self.accumulator_id, self.summ)
