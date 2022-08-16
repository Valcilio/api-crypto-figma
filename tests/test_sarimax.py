import pandas as pd
from pandas.testing import assert_frame_equal
import pickle

from domain.use_cases.sarimax import Sarimax

df_test_nopred = pd.read_csv('tests/test_data/test_csv_no_pred.csv').drop('Unnamed: 0', axis=1)
df_test_pred = pd.read_csv('tests/test_data/test_csv_with_pred.csv').drop('Unnamed: 0', axis=1)


ts_model = Sarimax(df=df_test_nopred, y='log1p_close')
model = ts_model.fit_sarimax()

def test_forecast_sarimax():
    '''Test default model (last) forecasting from the method forecast'''
    
    df_pred = ts_model.forecast()

    assert_frame_equal(df_test_pred, df_pred)

def test_forecast_sarimax_with_model_passed():
    '''Test forecast with passing a fitted model'''

    df_pred = ts_model.forecast(fitted_model=model)

    assert_frame_equal(df_test_pred, df_pred)
