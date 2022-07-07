import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

from resources.logger_msg import LoggerMsg

class Sarimax():

    def __init__(self, df: pd.DataFrame, **kwargs):

        self.df = df.copy()
        self.logger = LoggerMsg('TSModel')

    def fit_sarimax(self, passed_order: tuple = (2, 1, 5), seas_order: tuple = (1, 1, 1, 24), **kwargs):
        '''Fit sarimax model'''

        warnings.filterwarnings("ignore")
        self._definy_inferred_freq()
        model=SARIMAX(self.df, order=passed_order, seasonal_order=seas_order, **kwargs)
        self.fitted_model = model.fit(disp=0)

        return self.fitted_model

    def forecast(self, base_days: int = None, fitted_model = False, old_days: int = 0, next_days: int = 15, **kwargs):
        '''Use fitted model to forecasting. If don't has any fitted model
        passed, will use some model in the class, if don't exist too, will
        raise a error saying that is needed a fitted model to predict'''

        if base_days == None:
            base_days = len(self.df)
        
        try:
            if fitted_model:
                df_forecast = pd.DataFrame(fitted_model.predict(start=base_days + old_days, end=base_days
                                                                + next_days, dynamic=True), **kwargs)
            else:
                df_forecast = pd.DataFrame(self.fitted_model.predict(start=base_days + old_days, end=base_days
                                                                     + next_days, dynamic=True), **kwargs)
        except:
            self.logger.full_error("Call a 'fit_' method before this or pass a time series fitted model!")

        df_with_forecast = pd.concat([self.df, df_forecast], axis=1).rename(columns={'predicted_mean':f'{self.df.name}_forecast'})
        
        return df_with_forecast

    def _definy_inferred_freq(self, **kwargs):
        '''Inferred frequency definying to modeling'''

        self.df.index = pd.DatetimeIndex(self.df.index.values, 
                                    freq=self.df.index.inferred_freq)