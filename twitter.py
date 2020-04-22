import locale
from despesas import Despesas
from despesas_stats import Stats


def twitter():

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    despesas_getter = Despesas()

    value_column = {'empenho': 'ValorEmitido',
                    'liquidacao': 'ValorTransacao',
                    'pagamento': 'ValorTransacao'}

    operations = {'sum': 'valor total',
                  'max': 'maior valor',
                  'mean': 'valor médio dos valores',
                  'std': 'desvio padrão dos valores'}

    for despesa_type in ['empenho', 'liquidacao', 'pagamento']:
        df = despesas_getter.get_despesa_data(despesa_type)
        stat_results = Stats(df).get_total_despesas_stats(value_column[despesa_type], operations.keys())

        message = f'Despesas acumuladas no mês de {despesas_getter.current_date.strftime("%B")}, '\
                  f'até o dia {despesas_getter.current_date.day}, com {despesa_type}:\n'

        for stat_name, stat_value in stat_results.items():
            money_value = locale.currency(stat_value, grouping=True)
            message += f'{operations[stat_name]}: {money_value}\n'

        print(message.strip())
