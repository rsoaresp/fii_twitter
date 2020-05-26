from typing import Dict, List
from pandas import DataFrame


class Stats:

    def __init__(self, df: DataFrame):
        self.df = df

    def get_total_despesas_stats(self, column_name: str, operations: List[str]) -> Dict[str, float]:

        response = dict()
        for operation in operations:
            response[operation] = self.df[column_name].agg(operation)

        return response

    def get_top_despesas_by_criteria(self, column_name: str, group: str, operations: List[str]):

        top_cinco_gastos = self.df.groupby(group)[column_name].agg(operations)
        top_cinco_gastos = top_cinco_gastos.reset_index().sort_values(by='sum', ascending=False).head(6)

        return top_cinco_gastos