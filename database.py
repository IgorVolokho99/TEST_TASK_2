import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Base, Counter, CombinedResult

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Database:
    def __init__(self, session_factory: Session):
        self.Session = session_factory

    def add_counter(self, counter: Counter):
        session = self.Session()
        try:
            session.add(counter)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

    def get_all_counters(self):
        session = self.Session()
        try:
            return session.query(Counter).all()
        finally:
            session.close()

    def get_average_by_counter(self):
        session = self.Session()
        try:
            result = session.query(
                Counter.counter,
                func.avg(Counter.cell_1).label('avg_cell_1'),
                func.avg(Counter.cell_2).label('avg_cell_2'),
                func.avg(Counter.cell_3).label('avg_cell_3'),
                func.avg(Counter.cell_4).label('avg_cell_4')
            ).group_by(Counter.counter).all()
            return result
        finally:
            session.close()

    def count_null_cells(self):
        session = self.Session()
        try:
            result = session.query(
                Counter.counter,
                func.count().filter(
                    (Counter.cell_1 == None) |
                    (Counter.cell_2 == None) |
                    (Counter.cell_3 == None) |
                    (Counter.cell_4 == None)
                ).label('null_count')
            ).group_by(Counter.counter).all()
            return result
        finally:
            session.close()

    def get_combined_avg_and_null_count(self):
        session = self.Session()
        try:
            avg_subquery = session.query(
                Counter.counter,
                func.avg(Counter.cell_1).label('avg_cell_1'),
                func.avg(Counter.cell_2).label('avg_cell_2'),
                func.avg(Counter.cell_3).label('avg_cell_3'),
                func.avg(Counter.cell_4).label('avg_cell_4')
            ).group_by(Counter.counter).subquery()

            null_count_subquery = session.query(
                Counter.counter,
                func.count().filter(
                    (Counter.cell_1 == None) |
                    (Counter.cell_2 == None) |
                    (Counter.cell_3 == None) |
                    (Counter.cell_4 == None)
                ).label('null_count')
            ).group_by(Counter.counter).subquery()

            result = session.query(
                avg_subquery.c.counter,
                avg_subquery.c.avg_cell_1,
                avg_subquery.c.avg_cell_2,
                avg_subquery.c.avg_cell_3,
                avg_subquery.c.avg_cell_4,
                null_count_subquery.c.null_count
            ).outerjoin(
                null_count_subquery, avg_subquery.c.counter == null_count_subquery.c.counter
            ).all()

            return result
        finally:
            session.close()

    def save_combined_results(self, combined_results: tuple[CombinedResult]):
        session = self.Session()
        try:
            for row in combined_results:
                combined_result = CombinedResult(
                    counter=row.counter,
                    avg_cell_1=round(row.avg_cell_1, 0) if row.avg_cell_1 is not None else None,
                    avg_cell_2=round(row.avg_cell_2, 0) if row.avg_cell_2 is not None else None,
                    avg_cell_3=round(row.avg_cell_3, 0) if row.avg_cell_3 is not None else None,
                    avg_cell_4=round(row.avg_cell_4, 0) if row.avg_cell_4 is not None else None,
                    null_count=row.null_count
                )
                session.add(combined_result)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

    def get_saved_combined_results(self):
        session = self.Session()
        try:
            results = session.query(CombinedResult).all()
            return results
        finally:
            session.close()

    def clear_table_counter(self):
        session = self.Session()
        try:
            session.query(Counter).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

    def clear_table_combined_result(self):
        session = self.Session()
        try:
            session.query(CombinedResult).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()
