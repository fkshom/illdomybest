from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import UniqueConstraint, PrimaryKeyConstraint
# https://docs.sqlalchemy.org/en/13/core/type_basics.html#generic-types
from sqlalchemy.types import Integer, String, Boolean, Date

engine=create_engine("sqlite:///sqlite.db")
Base=declarative_base()
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    enable = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User id:{self.id} name:{self.name} enable:{self.enable}>'

class DoToday(Base):
    __tablename__ = "dotoday"
    date = Column(Date, primary_key=True, sqlite_on_conflict_unique='IGNORE', sqlite_on_conflict_primary_key='IGNORE')
    id = Column(Integer, primary_key=True, sqlite_on_conflict_unique='IGNORE', sqlite_on_conflict_primary_key='IGNORE')
    dotoday = Column(Boolean, default=False)
    PrimaryKeyConstraint('date', 'id', sqlite_on_conflict='IGNORE')
    UniqueConstraint('date', 'id', sqlite_on_conflict='IGNORE')
    def __repr__(self):
        return f'<User date:{self.date} id:{self.id} dotoday:{self.dotoday}>'
        
Base.metadata.create_all(engine)

SessionClass=sessionmaker(engine) #セッションを作るクラスを作成
session=SessionClass()

