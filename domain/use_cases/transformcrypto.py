import pandas as pd

from domain.entities.currencies import Currencies
from resources.logger_msg import LoggerMsg

class TransformCrypto(Currencies):

    def __init__(self, date_col: str, crypto: str, df: pd.DataFrame, 
                 market_curr: str):

        super().__init__(df=df, crypto_curr=crypto, market_curr=market_curr)

        self.df = df
        self.date_col = date_col
        self.crypto_market_curr = self.unify_crypto_market_curr()
        self.crypto = self.crypto_market_curr['crypto_curr']
        self.market_curr = self.crypto_market_curr['market_curr']
        self.orig_cols = ['timestamp', f'open ({self.market_curr})', f'high ({self.market_curr})', 
                          f'low ({self.market_curr})', f'close ({self.market_curr})', 'volume']

        self.logger = LoggerMsg(file_name='Transform')

    def run(self, **kwargs):
        self._run_transformations()
        self._run_business_rules()
        self._run_index_transformations()

        return self.df

    def _run_transformations(self, **kwargs):
        self._clean_cryptocurrency_data()
        self._rename_columns()

    def _run_business_rules(self, **kwargs):
        self.adjust_dtypes()
        self.check_columns()

    def _run_index_transformations(self, **kwargs):
        self._change_to_datetime_index()

    def _clean_cryptocurrency_data(self, **kwargs):
        '''Filter the dataframe to just contain the important columns to procedure
        with the next steps'''

        self.logger.init_data_transform(name=f'{self.crypto} historical data')
        self.df = self.df[self.orig_cols]

        return self.df

    def _rename_columns(self, **kwargs):
        '''Rename columns to a default name for future process'''

        name_cols = {f'open ({self.market_curr})':'open', f'high ({self.market_curr})':'high', 
                    f'low ({self.market_curr})':'low', f'close ({self.market_curr})':'close'}

        self.df = self.df.rename(columns=name_cols)

        return self.df

    def _change_to_datetime_index(self, **kwargs):
        '''Change set timestamp column to the index and change it into datetimeindex'''

        self.df = self.df.set_index(self.date_col).sort_index()
        self.df.index = pd.to_datetime(self.df.index)

        return self.df