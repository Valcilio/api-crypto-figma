import datetime as dt
import logging
from multiprocessing.sharedctypes import Value
from pandas.core.frame import DataFrame

from resources.context import Context

class LoggerMsg():

    def __init__(self, file_name: str, **kwargs):
        
        set_paths = Context()
        PROJ_DIR = set_paths.set_proj_path()
        LOG_FLD = set_paths.create_log_fld()
        self.today = dt.datetime.now().strftime('%Y%m%d')
        handlers = [
        logging.StreamHandler()
        ]

        logging.basicConfig(
            format='%(name)s || %(asctime)s (%(levelname)s) || %(message)s',
            level=logging.INFO,
            handlers=handlers
            )

        self.logger = logging.getLogger(file_name)

    def full_warning(self, msg: str, **kwargs):
        '''Send a warning message who is fully writed by the coder'''

        self.logger.warning(msg)

        return Warning(msg)

    def full_error(self, msg: str, **kwargs):
        '''Send a error message who is fully writed by the coder'''

        self.logger.error(msg)

        raise ValueError(msg)

    def init_extract(self, name: str, **kwargs):
        '''Send a warning message indicating the start of 
        the data extraction process'''

        msg = f'''Initing extract of {name}!'''
        self.logger.info(msg)

        return Warning(msg)

    def init_data_transform(self, name: str, **kwargs):
        '''Send a warning message indicating the start of 
        the data transformation process'''

        msg = f'''Initing data transform of {name}!'''
        self.logger.info(msg)

        return Warning(msg)

    def generic_error(self, name: str, **kwargs):
        '''Send a error message indicating a generic error'''

        msg = f'''Generic error in {name}, check the code!'''
        self.logger.error(msg)

        raise ValueError(msg)

    def warning_limit_rows(self, df: DataFrame, name: str, limit: int, **kwargs):
        '''Send a warning message when the dataset has a different quantity of
        rows than waited'''

        if df.shape[0] != limit:

            msg = f'''Extracting less rows from {name} than waited ({limit} != {df.shape[0]})!'''
            self.logger.warning(msg)
            
            return Warning(msg)

    def error_limit_cols(self, df: DataFrame, name: str, limit: int, **kwargs):
        '''Send a error message when the dataset has a differente quantity of
        columns than waited'''

        if df.shape[1] != limit:

            msg = f'''Extracting diferent quantity of columns from {name} than expected ({limit} != {df.shape[1]})!'''
            self.logger.error(msg)

            raise ValueError(msg)

    def end_msg(self, name: str, **kwargs):
        '''Send a warning message indicating when a process is finished'''

        msg = f'''{name} finished!'''
        self.logger.info(msg)

        return Warning(msg)

    def needed_error(self, var: str, options: str, **kwargs):
        '''Send a error message indicating when a variable don't correspond with
        the options passed'''

        msg = f'''{var} need to be in {options}!'''
        self.logger.error(msg)

        raise ValueError(msg)