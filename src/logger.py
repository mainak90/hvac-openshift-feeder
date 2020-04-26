import logging
import os


def setLevel():
    level = os.environ['LOGLEVEL'] if 'LOGLEVEL' in os.environ else 'INFO'
    if level == 'WARNING':
        return logging.basicConfig(filename='app.log', filemode='a', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    elif level == 'INFO':
        return logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    elif level == 'DEBUG':
        return logging.basicConfig(filename='app.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(process)d - LEVEL: %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
