import numpy as np

from domain.gateways.mainapi import MainAPI

framework_json = {'crypto': 'BTC', 
                'market_curr': 'USD', 
                'run_model': True,
                'column': 'open',
                'old_days': 0,
                'next_days': 14}

api_run = MainAPI(framework_json=framework_json)
api_df = api_run._full_data()

def test_columns():
    '''Test if all columns are in the df'''

    columns = ['timestamp', 'open', 'open_forecast']
    print(api_df)
    api_columns = list(api_df.columns)

    assert columns == api_columns

def testing_dtypes():
    '''Test if is returning the correct data types on columns'''

    print(api_df.dtypes)
    api_dtypes_dict = dict(api_df.dtypes)
    correct_dtypes = {
                'timestamp': np.dtype(object),
                'open': np.dtype('float64'),
                'open_forecast': np.dtype('float64'),
                }

    assert api_dtypes_dict == correct_dtypes

def testint_shape():
    '''Test if dataframe is returning correct shape'''
    assert api_df.shape == (1015, 3)