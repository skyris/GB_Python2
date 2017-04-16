from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
engine = create_engine("sqlite:///:memory:", echo=True)
Session.configure(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name={} fullname={} password={})" \
            .format(self.name, self.fullname, self.password)


# print(repr(User.__table__))


Base.metadata.create_all(engine)

ed_user = User(name="Ed", fullname="Ed Jounes", password="edpassword")

session.add(ed_user)
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')
])


ed_user.password = ";lkjsdf98"
print(repr(session.dirty))
# our_user = session.query(User).filter_by(name="Ed").first()
# print(our_user.fullname)

session.commit()