from typing import Dict, List
from pandas import DataFrame


class Stats:

    def __init__(self, df: DataFrame):
        self.df = df

    def get_total_despesas_stats(self, column_name: str, operations: List[str]) -> Dict[str, float]:

        response = dict()
        for operation in operations:
            value = self.df[column_name].astype(float)
            response[operation] = value.agg(operation)

        return response
