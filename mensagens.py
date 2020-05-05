from typing import Dict
import itertools
import yaml
import locale
from despesas import Despesas
from despesas_stats import Stats


class Mensagens:

    def __init__(self):
        self.despesas_getter = Despesas()
        self.config = load_configuration('configuration.yaml')

    def despesas_totais(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        for despesa_type in self.config['despesas_type']:
            df = self.despesas_getter.get_despesa_data(despesa_type)

            operations = self.config['operations'].keys()
            df_column_with_despesas = self.config['value_column'][despesa_type]
            stat_results = Stats(df).get_total_despesas_stats(df_column_with_despesas, operations)

            message = f'Gastos acumuladas em Campinas até {self.despesas_getter.data_hoje.strftime("%d-%m-%Y")}, com {despesa_type}:\n'

            for stat_name, stat_value in stat_results.items():
                money_value = locale.currency(stat_value, grouping=True)
                message += f'{self.config["operations"][stat_name]}: {money_value}\n'

            yield message.strip()

    def top_gastos(self):

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for despesa_type in self.config['despesas_type']:
            df = self.despesas_getter.get_despesa_data(despesa_type)

            operations = list(self.config['operations'].keys())
            df_column_with_despesas = self.config['value_column'][despesa_type]
            stat_results = Stats(df).get_despesas_unidade_gestora(df_column_with_despesas, operations)

            message = f'Os maiores gastos até {self.despesas_getter.data_hoje.strftime("%d-%m-%Y")}, agrupados por unidade gestora, com {despesa_type} foram:\n'

            for pos, row in enumerate(stat_results.iterrows()):
                yield message
                money_value_max = locale.currency(row[1]['max'], grouping=True)
                money_value_sum = locale.currency(row[1]['sum'], grouping=True)

                message = f"{1+pos} lugar: {row[1]['UnidadeGestoraDESC']} com gasto total de {money_value_sum} e maior valor de {money_value_max}\n"
                message = message.replace('SECRETARIA', 'SEC').replace('MUNICIPAL', 'MUN')


    def top_gastos_credor(self):

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for despesa_type in self.config['despesas_type']:
            df = self.despesas_getter.get_despesa_data(despesa_type)

            operations = list(self.config['operations'].keys())
            df_column_with_despesas = self.config['value_column'][despesa_type]
            stat_results = Stats(df).get_despesas_credor(df_column_with_despesas, operations)

            message = f'Os maiores gastos até {self.despesas_getter.data_hoje.strftime("%d-%m-%Y")}, por credor, com {despesa_type} foram:\n'

            for pos, row in enumerate(stat_results.iterrows()):
                yield message
                money_value_max = locale.currency(row[1]['max'], grouping=True)
                money_value_sum = locale.currency(row[1]['sum'], grouping=True)

                message = f"{1+pos} lugar: {row[1]['CredorDESC']} com gasto total de {money_value_sum} e maior valor de {money_value_max}\n"


def load_configuration(config_name: str) -> Dict[str, str]:
    """Load the configuration from a yaml file."""

    with open(config_name) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config