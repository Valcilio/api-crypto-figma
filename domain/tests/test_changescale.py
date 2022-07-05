import pandas as pd
from pandas.testing import assert_frame_equal

from domain.use_cases.changescale import ChangeScale

df_test = pd.read_csv('domain/tests/test_data/test_df.csv')
all_methods = ('box-cox', 'yeo-johnson', 'min-max', 'robust-scaler', 'log1p')

def test_rescaling():
    '''Test rescaling options to know if it's not rescaling for a different
    from asked'''
        
    for method in all_methods:
        y = 'close'
        change_scale = ChangeScale(df=df_test, y=y, method=method)
        df, scaler = change_scale.rescaling()
        df1, scaler1 = change_scale.rescaling()

        return assert_frame_equal(df, df1)

def test_inverse_transformation():
    '''Run test inverse transformation with the scale passed to guarantee that is
    possible to undo the transformation with no big differences'''

    for method in all_methods:
        y = 'close'
        change_scale = ChangeScale(df=df_test, y=y, method=method)
        df, scaler = change_scale.rescaling()
        df = change_scale.inverse_transformation(y_nt=f'{method}_{y}', scaler=scaler)
        df['orig_col'] = df_test[y]
        dif_nt = (df['orig_col'] - df[f'{method}_{y}_reversed']).mean()

        assert dif_nt < 0.01