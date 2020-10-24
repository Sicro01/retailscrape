import os # type: ignore
from datetime import datetime # type: ignore
from pathlib import Path # type: ignore
import logging # type: ignore

def get_timestamp():
    today = datetime.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H-%M-%S")
    return today + '_' + now

def get_filename(*args, appname='retailscrape', basedir=os.getcwd(), typeoffile='log', suffix='.log', sep='_', mid=''):
    # Build path and create dir
    # targetdir is one folder up from current working dir
    targetdir = os.path.dirname(basedir)
    filepath = os.path.join(targetdir, typeoffile)
    try:
        os.mkdir(filepath)
    except FileExistsError:
        pass
    # Build filename
    mid = ''.join((str(value)) for value in args)
    filename = appname + sep + typeoffile + sep + mid + sep + get_timestamp()
    # Join path and name
    filepathandname = Path(filepath, filename).with_suffix(suffix)
    return filepathandname

def log_remove_handlers(log):
    log.info('log_remove_handlers: Removing all existing log handlers')
    # get all loggers
    loggers = [logging.getLogger(name) if 'retail' in name else None for name in logging.root.manager.loggerDict]
    # for each valid logger remove all handlers
    for log in loggers:
        if log != None:
            while bool(len(log.handlers)):
                for handler in log.handlers:
                    log.removeHandler(handler)
# set up log
def create_log(module_name):
    log = logging.getLogger(module_name)
    log.info('create_log: Creating new log')
    return log
    
def setup_log(log,  search_term, level='DEBUG',):
    log_remove_handlers(log)
    log.setLevel(level)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, date_format)
    log_filenpathandame = get_filename(search_term, typeoffile='log', suffix='.log')
    log_write_mode = 'w+'
    file_handler = logging.FileHandler(log_filenpathandame, log_write_mode)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    log.info('set_up_log: Log configured')
    return log