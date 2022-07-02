from datetime import datetime
import pandas as pd

from use_cases.entities.resources.logger_msg import LoggerMsg
from use_cases.transformcrypto import TransformCrypto

class CryptocurrencyEtl():

    def __init__(self, api_key: str, crypto: str, market_curr: str,
                 start_date: str, end_date: str = datetime.now().strftime('%Y-%m-%d'), 
                date_col: str = 'timestamp', **kwargs):

        self.api_key = api_key
        self.crypto = crypto
        self.market_curr = market_curr
        self.start_date = start_date
        self.end_date = end_date
        self.date_col = date_col

        self.orig_cols = ['timestamp', f'open ({self.market_curr})', f'high ({self.market_curr})', 
                          f'low ({self.market_curr})', f'close ({self.market_curr})', 'volume']

        self.logger = LoggerMsg(file_name='Extract')

    def _extract_cryptocurrency_data(self, activate_errors_msg = True, **kwargs):
        '''Extract the cryptocurrency historical data from the API selected and
        check if has the quantity of rows and cols correct to go for the next step.'''

        self.logger.init_extract(name=f'ETL to obtain {self.crypto} historical data in {self.market_curr} value')
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={self.crypto}&market={self.market_curr}&apikey={self.api_key}&datatype=csv'
        self.df = pd.read_csv(url)

        if activate_errors_msg:
            self.logger.warning_limit_rows(df=self.df, name=f'Alpha Vantage API', limit=1000)
            self.logger.error_limit_cols(df=self.df, name=f'Alpha Vantage API', limit=11)

        return self.df

    def _filter_date(self, **kwargs):
        self.df = self.df[(self.df[self.date_col] >= self.start_date)
                         & (self.df[self.date_col] <= self.end_date)]