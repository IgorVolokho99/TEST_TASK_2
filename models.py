from sqlalchemy import Column, Integer, String, Sequence, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Counter(Base):
    __tablename__ = "counters"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    counter = Column(String(15))
    hour = Column(Integer)
    minute = Column(Integer)
    cell_1 = Column(Float)
    cell_2 = Column(Float)
    cell_3 = Column(Float)
    cell_4 = Column(Float)


class CombinedResult(Base):
    __tablename__ = "combined_results"
    id = Column(Integer, Sequence('combined_result_id_seq'), primary_key=True)
    counter = Column(String(15))
    avg_cell_1 = Column(Float)
    avg_cell_2 = Column(Float)
    avg_cell_3 = Column(Float)
    avg_cell_4 = Column(Float)
    null_count = Column(Integer)
