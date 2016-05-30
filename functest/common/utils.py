import logging
import logging.handlers

def get_item(keys, _dict):
    res_dict = dict(_dict)
    for k in keys:
	if res_dict:
	    res_dict = res_dict.get(k)
    return res_dict

def initialize_logger(log_file_name):
    log_format = '%(levelname)s %(asctime)s [%(filename)s %(funcName)s %(lineno)d]: %(message)s'
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger(log_file_name)
    filehandler = logging.handlers.RotatingFileHandler(
              log_file_name, maxBytes=10000000, backupCount=5)
    filehandler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(filehandler)
    return logger

def get_status_code(resp):
    return resp.get("Status") == 200


