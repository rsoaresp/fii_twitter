import requests
import pandas as pd
from pandas import DataFrame
from datetime import datetime


class Despesas:

    def __init__(self):
        self.current_date = datetime.today()
        self.base_url = "https://transparencia.campinas.sp.gov.br/index.php?"

    def get_despesa_data(self, despesa_type: str) -> DataFrame:

        url_address = self.get_despesa_request_str(despesa_type)
        response = requests.get(url_address)

        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            raise Exception('Could not perform get operation')

    def get_despesa_request_str(self, despesa_type: str) -> str:

        if despesa_type not in ['empenho', 'liquidacao', 'pagamento']:
            raise Exception('Invalid despesa type')

        despesa_str = f'action=ws&mode=getDespesas' \
                      f'&ano={self.current_date.year}' \
                      f'&mesinicio={self.current_date.month}' \
                      f'&mestermino={self.current_date.month}' \
                      f'&tipotr={despesa_type}'

        return f'{self.base_url}{despesa_str}'
