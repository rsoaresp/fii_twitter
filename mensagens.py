import itertools
import locale
import yaml
from typing import Dict
from pandas import DataFrame

from despesas import Despesas, Clean
from despesas_stats import Stats
from utils import config_loader


class Mensagens:

    def __init__(self):
        self.clean = Clean()
        self.despesas_getter = Despesas()
        self.config = config_loader('configuration.yaml')

        self.data = self.get_data()

    def get_data(self) -> Dict[str, DataFrame]:
        response = dict()
        for despesa in self.config['despesa_types']:
            response[despesa] = self._get_cleaned_df(despesa)
        return response

    def _get_cleaned_df(self, despesa) -> DataFrame:
        response, df = self.despesas_getter.get_despesas_up_to_data(despesa)
        for method in [i for i in self.clean.__dir__() if i.startswith('parse')]:
            df = eval(f'self.clean.{method}(df)')
        return df

    def total_despesas(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        for despesa in self.config['despesa_types']:

            operations = self.config['operations'].keys()
            despesa_column_name = self.config['value_column'][despesa]

            df = self.data[despesa]
            stat_results = Stats(df).get_total_despesas_stats(despesa_column_name, operations)

            message = self._total_despesas_message(despesa, stat_results)
            yield message

    def _total_despesas_message(self, despesa: str, stat_results: Dict[str, float]) -> str:

        message = f'Gastos acumulados em Campinas até {self.despesas_getter.data.strftime("%d-%m-%Y")}, com {despesa}:\n'
        for stat_name, stat_value in stat_results.items():
            money_value = locale.currency(stat_value, grouping=True)
            message += f'{self.config["operations"][stat_name]}: {money_value}\n'
        return message.strip()

    def top_gastos(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        for despesa in self.config['despesa_types']:

            operations = list(self.config['operations'].keys())
            despesa_column_name = self.config['value_column'][despesa]

            df = self.data[despesa]
            stat_results = Stats(df).get_top_despesas_by_criteria(despesa_column_name, 'UnidadeGestoraDESC', operations)

            message = f'Os maiores gastos até {self.despesas_getter.data.strftime("%d-%m-%Y")}, agrupados por unidade gestora, com {despesa} foram:\n'

            for pos, row in enumerate(stat_results.iterrows()):
                yield message
                money_value_max = locale.currency(row[1]['max'], grouping=True)
                money_value_sum = locale.currency(row[1]['sum'], grouping=True)

                message = f"{1+pos} lugar: {row[1]['UnidadeGestoraDESC']} com gasto total de {money_value_sum} e maior valor de {money_value_max}\n"
                message = message.replace('SECRETARIA', 'SEC').replace('MUNICIPAL', 'MUN')

    def top_gastos_credor(self):

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for despesa in self.config['despesa_types']:

            operations = list(self.config['operations'].keys())
            df_column_with_despesas = self.config['value_column'][despesa]

            df = self.data[despesa]
            stat_results = Stats(df).get_top_despesas_by_criteria(df_column_with_despesas, 'CredorDESC', operations)

            message = f'Os maiores gastos até {self.despesas_getter.data.strftime("%d-%m-%Y")}, por credor, com {despesa} foram:\n'

            for pos, row in enumerate(stat_results.iterrows()):
                yield message
                money_value_max = locale.currency(row[1]['max'], grouping=True)
                money_value_sum = locale.currency(row[1]['sum'], grouping=True)

                message = f"{1+pos} lugar: {row[1]['CredorDESC']} com gasto total de {money_value_sum} e maior valor de {money_value_max}\n"