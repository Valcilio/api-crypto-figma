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
        sarimax_run = APISarimax(df = self.df,
                                old_days=self.old_days, 
                                next_days=self.next_days,
                                method = 'log1p')

        df_with_pred = sarimax_run.run_sarimax_pipeline()

        return df_with_pred

    def _filterdf(self, **kwargs):
        '''Filter dataframe to modeling'''

        self.df = pd.DataFrame(self.df[self.column])