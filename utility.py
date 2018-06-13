import logging

import vars

# Decorator
def log(func):
    def wrapper(*args, **kwargs):
        logging.debug('@ ', func.__name__)
        func(*args, **kwargs)
        logging.debug('$ ', func.__name__)

def chop(string):
    return string[1:-1]
