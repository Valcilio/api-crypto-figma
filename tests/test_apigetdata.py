import numpy as np

from domain.gateways.apigetdata import APIGetData

crypto = 'BTC'
market_curr = 'USD'
api_run = APIGetData(crypto=crypto, market_curr=market_curr)
api_df = api_run.extract_transform_data()

def test_columns():
    '''Test if all columns are in the df'''

    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    api_columns = list(api_df.reset_index().columns)

    assert columns == api_columns

def testing_dtypes():
    '''Test if is returning the correct data types on columns'''

    api_dtypes_dict = dict(api_df.dtypes)
    correct_dtypes = {
                'open': np.dtype('float64'),
                'high': np.dtype('float64'),
                'low': np.dtype('float64'),
                'close': np.dtype('float64'),
                'volume': np.dtype('int64')
                }

    assert api_dtypes_dict == correct_dtypes

def testing_dateindex():
    '''Test if is returning the dateindex'''

    df_test = api_df.copy()
    df_test['test'] = 1
    df_test = df_test['test'].reset_index().select_dtypes('datetime64[ns]')
    dateindex_check = df_test.shape[1]

    assert dateindex_check == 1