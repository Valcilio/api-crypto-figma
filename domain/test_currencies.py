import numpy as np
import pandas as pd

from webui.gateways.use_cases.entities.currencies import Currencies

df_test = pd.read_csv('test_data/test_df.csv')
market_curr = 'BRL'
crypto_curr = 'ETH'
run_business_rules = Currencies(df=df_test, market_curr=market_curr, crypto_curr=crypto_curr)

def test_check_columns():
    '''Test if has all columns in dataframe'''
    run_business_rules.check_columns()

def test_transform_dtypes():
    '''Test if dtypes are correctly'''

    run_business_rules.adjust_dtypes()
    df_dtypes = {
                'timestamp': np.dtype('<M8[ns]'),
                'open': np.dtype('float64'),
                'high': np.dtype('float64'),
                'low': np.dtype('float64'),
                'close': np.dtype('float64'),
                'volume': np.dtype('float64')
                }

    df_dict_dtypes = dict(df_test.dtypes)

    assert df_dtypes == df_dict_dtypes

def test_crypto_market_curr():
    '''Test if is returning correctly the dict
    with cryptocurrency and market currency'''

    test_dict = {'crypto_curr': crypto_curr, 'market_curr': market_curr}
    crypto_market_curr = run_business_rules.unify_crypto_market_curr()

    assert test_dict == crypto_market_curr