import datetime as dt
import numpy as np
import pandas as pd
from   sklearn import preprocessing as pp

from .entities.resources.logger_msg import LoggerMsg

class ChangeScale():

    def __init__(self, df: pd.DataFrame, date_col: str = 'nan', 
                start_date: str = '2020-01-01', 
                end_date: str = dt.datetime.now().strftime("%Y-%m-%d"), **kwargs):

        self.start_date = start_date
        self.end_date = end_date
        self.df = df.copy()
        self.date_col = date_col
        self.logger = LoggerMsg(file_name='DataTrans')

    def rescaling(self, y: str, df: pd.DataFrame, method: str = 'yeo-johnson', **kwargs):
        '''Rescale the column passed as "y" to a scale who was passed in "method" attribute
        and check if this transformation is correct with the method "test_rescale"'''

        df = df.copy()

        if method in ['box-cox', 'yeo-johnson']:
            scaler = pp.PowerTransformer(method=method)
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'min-max':
            scaler = pp.MinMaxScaler()
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'robust-scaler':
            scaler = pp.RobustScaler()
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'log1p':
            scaler = 'log1p'
            df[f'{method}_{y}'] = np.log1p(df[y])
        else:
            self.logger.needed_error(var = "Method", options="['box-cox', 'yeo-johnson', 'min-max', 'robust-scaler', 'log1p']")

        self.test_rescale(y=y, method=method, scaler=scaler, df=df)
        df = df.drop(y, axis=1)

        return df, scaler

    def inverse_transformation(self, df: pd.DataFrame, col_orig_name: str, y_nt: str, scaler, **kwargs):
        '''Undo the rescaling based in the scaler passed'''

        df = df.copy()
        df[f'{col_orig_name}'] = df[y_nt]
        df = df.drop(y_nt, axis=1)

        try:
            if scaler == 'log1p':
                df[f'{y_nt}_reversed'] = np.expm1(df[f'{col_orig_name}'])
            else:
                df[f'{y_nt}_reversed'] = scaler.inverse_transform(df[[f'{col_orig_name}']])
        except:
            self.logger.full_error("Check scaler passed!")

        return df.drop(col_orig_name, axis=1)

    def test_rescale(self, method: str, scaler, df: pd.DataFrame, y: str, **kwargs):
        '''Run test inverse transformation with the scale passed to guarantee that is
        possible to undo the transformation with no big differences'''

        df = df.copy()
        df['orig_col'] = df[y]
        df = self.inverse_transformation(df=df, col_orig_name=y, y_nt=f'{method}_{y}', scaler=scaler) 
        dif_nt = (df['orig_col'] - df[f'{method}_{y}_reversed']).mean()

        if dif_nt > 0.01:
            self.logger.generic_error(f"Nature Transformation ({method})")
        elif (dif_nt < 0.01) & (dif_nt > 0):
            self.logger.full_warning(f'''The mean difference in {method} transformation 
                                         is below 0.01! (difference = {dif_nt})''')

    def prepare_dataframe_timeseries(self, y: str, method: str = 'yeo-johnson', exogenous: list = False, **kwargs):
        '''Prepare the timeserie to the modeling process'''
        
        df = self.check_transform_dateindex()
        df, scaler = self.rescaling(df=df, y=y, method=method)
        df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)

        if exogenous:
            exogenous.append(f'{method}_{y}')
            df = df[exogenous]            
        else:
            df = df[f'{method}_{y}']

        return df, scaler