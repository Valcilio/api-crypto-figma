from pandas.testing import assert_frame_equal
import pickle

from domain.use_cases.sarimax import Sarimax

df_test_nopred = pickle.load(open('domain/tests/test_data/test_csv_no_pred.pkl', 'rb'))
df_test_pred = pickle.load(open('domain/tests/test_data/test_csv_with_pred.pkl', 'rb'))

ts_model = Sarimax(df=df_test_nopred)
model = ts_model.fit_sarimax()

def test_forecast_sarimax():
    '''Test default model (last) forecasting from the method forecast'''
    
    df_pred = ts_model.forecast()

    return assert_frame_equal(df_test_pred, df_pred)

def test_forecast_sarimax_with_model_passed():
    '''Test forecast with passing a fitted model'''

    df_pred = ts_model.forecast(fitted_model=model)

    return assert_frame_equal(df_test_pred, df_pred)