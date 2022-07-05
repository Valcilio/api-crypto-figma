import datetime as dt
import pandas as pd

from domain.resources.logger_msg import LoggerMsg

class Currencies():
	
    def __init__(self, df: pd.DataFrame, crypto_curr: str, market_curr: str, **kwargs):
        
        self.df = df
        self.crypto_curr = crypto_curr
        self.market_curr = market_curr

        self.logger = LoggerMsg('Entities')
        self.currency_cols = ['close', 'open', 'high', 'low', 'volume']

    def check_columns(self, **kwargs):
        '''Business rule, currency need to have this informations'''

        cols_check = list(self.df.columns)
        test_cols = self.currency_cols + ['timestamp']

        assert all(item in test_cols for item in cols_check)

    def adjust_dtypes(self, **kwargs):
        '''Business rule, any cryptocurrency will have timestamp,
        open, close, high, low and volume with the current astype below'''

        currency_cols = self.currency_cols
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df[currency_cols] = self.df[currency_cols].astype(float)

    def unify_crypto_market_curr(self, **kwargs):
        '''Business rule, each cryptocurrency will be given in market currency value, then
        for each cryptocurrency will exist a market_curr'''
        
        crypto_market_curr = {'crypto_curr': self.crypto_curr, 'market_curr': self.market_curr}

        return crypto_market_curr
    
