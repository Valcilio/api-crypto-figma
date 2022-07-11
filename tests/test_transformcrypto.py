import os
import pandas as pd
import pytest
from random import choice
from domain.use_cases.transformcrypto import TransformCrypto

df_test = pd.read_csv('tests/test_data/test_df.csv')

crypto = choice(('BTC', 'ETH', 'ADA', 'DOGE', 'XRP'))
market_curr = choice(('USD', 'BRL', 'CNY', 'EUR', 'GBP'))
api_key = os.environ.get('TOKEN_FIGMA_CRYPTO_KEY')

orig_cols = ['timestamp', f'open ({market_curr})', f'high ({market_curr})', 
            f'low ({market_curr})', f'close ({market_curr})', 'volume']

df_test.columns = orig_cols
df_test['dirt'] = 1

trans_crypto = TransformCrypto(df=df_test, date_col='timestamp', 
                            crypto=crypto,
                            market_curr=market_curr)

def test_clean_cryptocurrency_data():
    '''Test if the data extract has the correct columns shape'''

    orig_cols = ['timestamp', f'open ({market_curr})', f'high ({market_curr})', 
                f'low ({market_curr})', f'close ({market_curr})', 'volume']

    df = trans_crypto._clean_cryptocurrency_data()
    df_cols = list(df.columns)

    assert df_cols == orig_cols

def test_rename_columns():
    '''Test if the columns has the correct name'''

    name_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

    df = trans_crypto._rename_columns()
    df_cols = list(df.columns)

    assert df_cols == name_cols

def test_datetimeindex():
    '''Test if the index changed to datetime index'''

    df = trans_crypto._change_to_datetime_index()
    df['test'] = 1
    df = df['test'].reset_index().select_dtypes('datetime64[ns]')
    dateindex_check = df.shape[1]

    assert dateindex_check == 1

def test_run():
    '''Testing '''

    df_test = pd.read_csv('tests/test_data/test_df.csv')
    df_test.columns = orig_cols
    df_test['dirt'] = 1

    trans_crypto = TransformCrypto(df=df_test, date_col='timestamp', 
                                crypto=crypto, 
                                market_curr=market_curr)
    trans_crypto.run()

    return print(df_test)