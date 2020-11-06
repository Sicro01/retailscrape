import logging # type: ignore
from classes.filename_class import Filename # type: ignore

class Log:
    def __init__(self, module_name='scrape', level='INFO'):
        self.module_name = module_name
        self.log = logging.getLogger(module_name)
        self.level = level
        self.log.setLevel(self.level)
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter(self.log_format, self.date_format)
        self.log_write_mode = 'w+'
        
    @property
    def log_filepathandname(self):
        f = Filename(typeofile='log', suffix='.log', folder_name='log', sep='_', filename_term=self.module_name)
        return f.filepathandname
    
    def log_addfh(self):
        self.file_handler = logging.FileHandler(self.log_filepathandname, self.log_write_mode)
        self.file_handler.setFormatter(self.formatter)
        self.log.addHandler(self.file_handler)
    
    def log_addch(self):
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.log.addHandler(self.console_handler)

    def log_remove_handlers(self):
        self.log.info('log_remove_handlers: Removing all existing log handlers')
        # get all loggers
        loggers = [logging.getLogger(name) if 'retail' in name else None for name in logging.root.manager.loggerDict]
        # for each valid logger remove all handlers
        for log in loggers:
            if log != None:
                while bool(len(log.handlers)):
                    for handler in log.handlers:
                        print('removing handler!')
                        log.removeHandler(handler)
