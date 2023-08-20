import sqlalchemy as db
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MemoryCard(Base):
    __tablename__ = 'memory_cards'

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String, nullable=False)
    back = db.Column(db.String, nullable=False)

    def __init__(self, front, back):
        self.front = front
        self.back = back

class Database:
    def __init__(self, db_uri='sqlite:///memory_cards.db'):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store_memory_card(self, front, back):
        session = self.Session()
        new_card = MemoryCard(front, back)
        session.add(new_card)
        session.commit()
        session.close()

    def get_all_memory_cards(self):
        session = self.Session()
        cards = session.query(MemoryCard).all()
        session.close()
        return cards
