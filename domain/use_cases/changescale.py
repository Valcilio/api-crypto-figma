import numpy as np
import pandas as pd
from   sklearn import preprocessing as pp
import warnings

class ChangeScale():

    def __init__(self, df: pd.DataFrame, y: str, method: str = 'yeo-johnson', **kwargs):

        self.df = pd.DataFrame(df.copy())
        self.method = method
        self.y = y

    def _fit_transform(self, scaler, df: pd.DataFrame, y: str, method: str, **kwargs):
        '''Fit, transform and return fitted scale and add scaled column to dataframe'''

        scaler = scaler.fit(df[[y]])
        df[f'{method}_{y}'] = scaler.transform(df[[y]])

        return scaler

    def rescaling(self, **kwargs):
        '''Rescale the column passed as "y" to a scale who was passed in "method" attribute
        and check if this transformation is correct with the method "test_rescale"'''

        df = self.df

        if self.method in ['box-cox', 'yeo-johnson']:
            scaler = pp.PowerTransformer(method=self.method)
            scaler = self._fit_transform(scaler=scaler, df=df, y=self.y, method=self.method)
        elif self.method == 'min-max':
            scaler = pp.MinMaxScaler()
            scaler = self._fit_transform(scaler=scaler, df=df, y=self.y, method=self.method)
        elif self.method == 'robust-scaler':
            scaler = pp.RobustScaler()
            scaler = self._fit_transform(scaler=scaler, df=df, y=self.y, method=self.method)
        elif self.method == 'log1p':
            scaler = 'log1p'
            df[f'{self.method}_{self.y}'] = np.log1p(df[self.y])

        df = df.drop(self.y, axis=1)

        return df, scaler

    def inverse_transformation(self, y_nt: str, scaler, **kwargs):
        '''Undo the rescaling based in the scaler passed'''

        warnings.filterwarnings('ignore')

        df = self.df
        df[f'{self.y}'] = df[y_nt]
        df = df.drop(y_nt, axis=1)

        if scaler == 'log1p':
            df[f'{y_nt}_reversed'] = np.expm1(df[f'{self.y}'])
        else:
            df[f'{y_nt}_reversed'] = scaler.inverse_transform(df[[f'{self.y}']])

        return df.drop(self.y, axis=1)