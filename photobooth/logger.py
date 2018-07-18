import logging

# create logger photobooth
logger = logging.getLogger('photobooth')
logger.setLevel(logging.DEBUG)

# create console handler and set level to INFO
console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to console_logger
console_logger.setFormatter(formatter)

# add console_logger to logger
logger.addHandler(console_logger)



glogger = logging.getLogger('gphoto2')
glogger.setLevel(logging.ERROR)

# create console handler and set level to INFO
gconsole_logger = logging.StreamHandler()
gconsole_logger.setLevel(logging.ERROR)

# create formatter
gformatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to console_logger
gconsole_logger.setFormatter(formatter)

# add console_logger to logger
glogger.addHandler(console_logger)
