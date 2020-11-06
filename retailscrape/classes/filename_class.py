import os # type: ignore
from pathlib import Path # type: ignore
from datetime import datetime # type: ignore
BASEDIR = 'C:\\Users\\simon\\Documents\\py_projects\\retailscrape\\retailscrape'

class Filename:
    def __init__(self, module_name='retailscrape', typeofile='log', suffix='.log', folder_name='logs', sep='_', filename_term=''):
        self.module_name = module_name
        self.typeofile = typeofile
        self.suffix = suffix
        self.folder_name = folder_name
        self.sep = sep
        self.filename_term = filename_term
        self.basedir = BASEDIR
        self.filepath = os.path.join(BASEDIR, self.folder_name)
        self.filename = self.module_name + self.sep + self.typeofile + self.sep + self.filename_term + self.sep + self.get_timestamp()
        self.filepathandname = Path(self.filepath, self.filename).with_suffix(self.suffix)
        self.make_dir()
    
    def __str__(self):
        return f'filepathandname:{str(self.filepathandname)}'
    
    def make_dir(self):
        # this_filepath = os.path.join(BASEDIR, self.filepath)
        try:
            os.mkdir(self.filepath)
        except FileExistsError:
            pass

    def get_timestamp(self):
        today = datetime.today().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H-%M-%S")
        return today + '_' + now
        