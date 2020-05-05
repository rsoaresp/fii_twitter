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

    def get_despesas_unidade_gestora(self, column_name: str, operations: List[str]):
        self.df[column_name] = self.df[column_name].astype(float)

        top_cinco_gastos = self.df.groupby('UnidadeGestoraDESC')[column_name].agg(operations)
        top_cinco_gastos = top_cinco_gastos.reset_index().sort_values(by='sum', ascending=False).head(6)

        top_cinco_gastos['UnidadeGestoraDESC'] = top_cinco_gastos['UnidadeGestoraDESC'].str.split('-').str.get(1)

        return top_cinco_gastos

    def get_despesas_credor(self, column_name: str, operations: List[str]):
        self.df[column_name] = self.df[column_name].astype(float)

        top_cinco_gastos = self.df.groupby('CredorDESC')[column_name].agg(operations)
        top_cinco_gastos = top_cinco_gastos.reset_index().sort_values(by='sum', ascending=False).head(6)

        top_cinco_gastos['CredorDESC'] = top_cinco_gastos['CredorDESC'].str.split(' - ').str.get(1)

        return top_cinco_gastos
