import html
from datetime import datetime
from typing import Optional, Tuple, Dict

import pandas as pd
import requests
from pandas import DataFrame

from utils import config_loader


class Despesas:

    def __init__(self, data: Optional[datetime] = None):
        self.data = data if data else datetime.today()
        self.config = config_loader('configuration.yaml')

    def get_despesas_up_to_data(self, despesa: str) -> Tuple[Dict, DataFrame]:

        url_address = self._get_despesa_request_str(despesa)
        response = requests.get(url_address)

        if response.status_code == 200:
            return response, pd.DataFrame(response.json())
        else:
            return response, pd.DataFrame()

    def _get_despesa_request_str(self, despesa: str) -> str:

        if despesa not in self.config['despesa_types']:
            raise Exception('Invalid despesa type')

        args = dict(despesa=despesa, year=self.data.year, month=self.data.month, begin=1)
        despesa_str = self.config['api']['actions'].format(**args)

        api_call_url = f"{self.config['api']['base_url']}{despesa_str}"

        return api_call_url


class Clean:

    def __init__(self):
        self.config = config_loader('configuration.yaml')

    def parse_string_columns(self, df: DataFrame) -> DataFrame:
        for column in self.config['cleaning']['str_columns_to_parse']:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: html.unescape(x)).astype(str)
        return df

    def parse_numeric_columns(self, df: DataFrame) -> DataFrame:
        for column in self.config['cleaning']['numeric_columns_to_parse']:
            if column in df.columns:
                df[column] = df[column].astype(float)
        return df

    def parse_dates(self, df: DataFrame) -> DataFrame:
        column = self.config['cleaning']['date_column']
        df[column] = pd.to_datetime(df[column], infer_datetime_format=True)
        return df
