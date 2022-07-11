import pandas as pd

from domain.use_cases.sarimax import Sarimax
from domain.use_cases.changescale import ChangeScale

class APISarimax():

    def __init__(self,
                df: pd.DataFrame,
                y: str,
                old_days: int = 0, 
                next_days: int = 15,
                method: str = 'log1p',
                **kwargs):

        self.df = df.copy()
        self.y = y
        self.old_days = old_days
        self.next_days = next_days
        self.method = method

    def run_sarimax_pipeline(self, **kwargs):
        '''Run all modeling pipeline and return df with pred'''

        self._change_scale()
        self._get_forecast()
        self._return_original_scales()
        self._return_original_names()

        return self.df

    def _change_scale(self, **kwargs):
        '''Change dataset to a better scale for modeling'''

        rescalling_df = ChangeScale(df=self.df, y=self.y, method=self.method)
        self.df, self.scaler = rescalling_df.rescaling()

        return self.df

    def _reverse_scale(self, y_it: str, y_nt: str, **kwargs):
        '''Reverse change of rescalling to original scale'''

        inv_trans_scale = ChangeScale(df=self.df, y=y_it, method=self.method)
        self.df = inv_trans_scale.inverse_transformation(y_nt=y_nt, scaler=self.scaler)

        return self.df

    def _return_original_scales(self, **kwargs):
        '''Return every variable to original scale'''

        y_forecast = self.y + '_forecast'
        self._reverse_scale(y_it = self.y, y_nt = f'{self.method}_{self.y}')
        self._reverse_scale(y_it = self.y, y_nt = y_forecast)

        return self.df

    def _return_original_names(self, **kwargs):
        '''Reverse to original names without modifications'''

        orig_names = {f'{self.method}_{self.y}_reversed': self.y,
                    f'{self.y}_forecast_reversed': self.y + '_forecast'}

        self.df.rename(columns=orig_names, inplace=True)

        return self.df

    def _get_forecast(self, **kwargs):
        '''Get forecast from SARIMAX'''

        self.sarimax = Sarimax(df=self.df, y=self.y)
        self.sarimax.fit_sarimax()
        self.df = self.sarimax.forecast(old_days=self.old_days, next_days=self.next_days)

        return self.df