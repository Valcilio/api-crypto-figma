import numpy as np
import pandas as pd
import pickle

from domain.gateways.apigetsarimax import APISarimax

df_test_nopred = pd.read_csv('tests/test_data/test_csv_no_pred.csv')
df_test_nopred = df_test_nopred.rename(columns={'Unnamed: 0':'timestamp'})
df_test_nopred['timestamp'] = pd.to_datetime(df_test_nopred['timestamp'])
df_test_nopred = df_test_nopred.set_index('timestamp')
df_test = pd.DataFrame(df_test_nopred)
df_test['close'] = np.expm1(df_test['log1p_close'])
df_test = df_test['close']
ts_model = APISarimax(df=df_test, y=df_test.name)
df_full = ts_model.run_sarimax_pipeline()

def test_cols_names():
    '''Test cols name'''

    cols_df_full = list(df_full.columns)
    expected_cols = ['close', f'close_forecast']

    assert cols_df_full == expected_cols

def test_dtypes():
    '''Test if is returning correct dtypes'''

    df_full_dtypes_dict = dict(df_full.dtypes)
    correct_dtypes = {
                'close': np.dtype('float64'),
                'close_forecast': np.dtype('float64')
                }

    assert df_full_dtypes_dict == correct_dtypes

def test_shape():
    '''Test if is returning correct df shape'''

    shape_df_full = df_full.shape

    assert shape_df_full == (193, 2)

def test_correct_scale():
    '''Test if is returning df with correct scale'''

    first_value = df_full.iloc[0, 0]

    assert first_value > 1000

def test_change_scale():
    '''Test if is rescalling data correctly'''

    check_scale = APISarimax(df=df_test, y=df_test.name)
    df_scale = check_scale._change_scale()
    value_scale = df_scale.iloc[0, 0]

    assert value_scale < 1000