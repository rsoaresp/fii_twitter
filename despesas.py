import html

import requests
import pandas as pd
from pandas import DataFrame
from datetime import datetime


class Despesas:

    def __init__(self):
        self.data_hoje = datetime.today()
        self.ano = self.data_hoje.year
        self.mes = self.data_hoje.month
        self.base_url = "https://transparencia.campinas.sp.gov.br/index.php?"

    def get_despesa_data(self, despesa_type: str) -> DataFrame:

        url_address = self._get_despesa_request_str(despesa_type)
        response = requests.get(url_address)

        df = pd.DataFrame(response.json())
        df = self._ajeita_colunas_string(df)
        df['mesAno'] = pd.to_datetime(df['mesAno'], infer_datetime_format=True)

        if response.status_code == 200:
            return df
        else:
            raise Exception('Could not perform get operation')

    def _ajeita_colunas_string(self, df):
        colunas_para_arrumar = ['UnidadeGestoraDESC', 'CredorDESC', 'NaturezaDESC']

        for coluna in colunas_para_arrumar:
            df[coluna] = df[coluna].apply(lambda x: html.unescape(x)).astype(str)
        return df

    def _get_despesa_request_str(self, tipo_despesa: str) -> str:

        if tipo_despesa not in ['empenho', 'liquidacao', 'pagamento']:
            raise Exception('Invalid despesa type')

        despesa_str = f'action=ws&mode=getDespesas&ano={self.ano}&mesinicio={1}&mestermino={self.mes}&tipotr={tipo_despesa}'

        api_call_url = f'{self.base_url}{despesa_str}'

        return api_call_url
