import os
import pandas as pd

from resources.logger_msg import LoggerMsg
from domain.use_cases.transformcrypto import TransformCrypto

class APIGetData():

    def __init__(self, crypto: str, market_curr: str,
                **kwargs):

        self.api_key = os.environ.get('TOKEN_FIGMA_CRYPTO_KEY')
        self.crypto = crypto
        self.market_curr = market_curr

        self.logger = LoggerMsg(file_name='APIGetData')

    def extract_transform_data(self, **kwargs):
        '''Run extract and transform methods'''

        self._extract_cryptocurrency_data()
        df = self._transform_dataset()

        return df

    def _extract_cryptocurrency_data(self, activate_errors_msg = True, **kwargs):
        '''Extract the cryptocurrency historical data from the API selected and
        check if has the quantity of rows and cols correct to go for the next step.'''

        self.logger.init_extract(name=f'ETL to obtain {self.crypto} historical data in {self.market_curr} value')
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={self.crypto}&market={self.market_curr}&apikey={self.api_key}&datatype=csv'
        self.df = pd.read_csv(url)

        if activate_errors_msg:
            self.logger.warning_limit_rows(df=self.df, name=f'Alpha Vantage API', limit=1000)
            self.logger.error_limit_cols(df=self.df, name=f'Alpha Vantage API', limit=11)

    def _transform_dataset(self, **kwargs):
        '''Derivate dataset to visuzalitions without prediction'''

        trans_crypto_data = TransformCrypto(df = self.df, 
                                            date_col = 'timestamp',
                                            crypto = self.crypto, 
                                            market_curr = self.market_curr)

        df = trans_crypto_data.run()

        return df
