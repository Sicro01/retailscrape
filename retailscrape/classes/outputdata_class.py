import pandas as pd # type: ignore
from classes.filename_class import Filename # type: ignore
from classes.product_class import Product # type: ignore

class OutputData:
    def __init__(self, class_=None, df=None, class_list=None, sort_columns=[], filename_term='term'):
        self.df = df
        self.class_ = class_
        self.class_list = class_list
        self.sort_columns = sort_columns
        self.filename_term = filename_term
        self.filename = Filename(typeofile='data', suffix='.csv', folder_name='data', sep='_', filename_term=self.filename_term)

    def save_list_as_df(self):
        # main_log.log.info(f'save_list_as_df: number of items being saved={len(self.list_of_items)}')
        # Convert class list to a df and prep it for output
        self.df = pd.DataFrame.from_records([item.to_dict() for item in self.class_list])

    def save_df_as_csv(self):
        # main_log.log.info(f'save_df_as_csv: number of items being saved={len(self.df)}')
        if bool(self.sort_columns):
            self.df.sort_values(by=self.sort_columns, inplace=True)
        self.df.columns = self.df.columns.str.strip().str.upper().str.replace(r'\s+', '_').str.replace('-', '_').str.replace('(', '').str.replace(')', '')
        self.df.to_csv(self.filename.filepathandname, index=False, sep=",")

    def df_to_class_list(self):
        self.df.columns = self.df.columns.str.lower()
        self.class_list = [self.class_(**kwargs) for kwargs in self.df.to_dict(orient='records')]
        self.df.columns = self.df.columns.str.upper()
        