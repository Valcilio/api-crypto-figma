import pandas as pd

from domain.gateways.apigetdata import APIGetData
from domain.gateways.apigetsarimax import APISarimax

class MainAPI():

    def __init__(self, framework_json, **kwargs):

        self.column = framework_json['column']

        self.crypto = framework_json['crypto']
        self.market_curr = framework_json['market_curr']

        self.run_model = framework_json['run_model']
        self.old_days = framework_json['old_days']
        self.next_days = framework_json['next_days']

    def run(self, **kwargs):

        if self.run_model:
            self.full_data()
        else:
            self.get_data()

        return self.df

    def full_data(self, **kwargs):
        '''Return all data'''

        self.get_sarimax_pred()
        self._transform_series_to_dataframes()
        self._concat_pred_with_orig_data()

        return self.df

    def get_data(self, **kwargs):
        '''Run API to get data'''

        api_get_data = APIGetData(crypto=self.crypto, 
                                market_curr=self.market_curr)
        self.df = api_get_data.extract_transform_data()
        self._filterdf()

        return self.df        

    def get_sarimax_pred(self, **kwargs):
        '''Get data and run model to return dataframe with forecast'''

        self.get_data()
        df_model = self.df.tail(150)
        sarimax_run = APISarimax(df = df_model,
                                y = self.column,
                                old_days=self.old_days, 
                                next_days=self.next_days,
                                method = 'log1p')

        self.df_with_pred = sarimax_run.run_sarimax_pipeline()

        return self.df_with_pred

    def _filterdf(self, **kwargs):
        '''Filter dataframe to modeling'''

        self.df = pd.DataFrame(self.df[self.column])

    def _transform_series_to_dataframes(self, **kwargs):
        '''Transform into dataframes for modeling'''

        self.df = pd.DataFrame(self.df)
        self.df_with_pred = pd.DataFrame(self.df_with_pred[f'{self.column}_forecast'])

    def _concat_pred_with_orig_data(self, **kwargs):
        '''Concat pred dataframe with full data'''

        self.df = pd.concat([self.df, self.df_with_pred], axis=1)