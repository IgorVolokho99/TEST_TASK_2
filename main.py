import json
from tabulate import tabulate

from database import Database, Session
from models import Counter


class Solution:
    def __init__(self, path: str):
        self.path = path
        self.init_db()

    def init_db(self):
        db = Database(Session)
        db.clear_table_counter()

        with open(self.path, 'r') as f:
            data = json.load(f)

        for kwargs in data:
            new_counter = Counter(
                **kwargs
            )
            db.add_counter(new_counter)

    def make_task(self):
        db = Database(Session)

        db.clear_table_combined_result()

        combined_results = db.get_combined_avg_and_null_count()
        db.save_combined_results(combined_results)

        combined_results = db.get_saved_combined_results()
        table_data = [
            [row.counter, row.avg_cell_1, row.avg_cell_2, row.avg_cell_3, row.avg_cell_4, row.null_count]
            for row in combined_results
        ]
        headers = ["Counter", "Avg Cell 1", "Avg Cell 2", "Avg Cell 3", "Avg Cell 4", "Null Count"]

        print("\nSaved Combined Results:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    obj = Solution("data.json")
    obj.make_task()
