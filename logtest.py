import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',filename='.\Logs\myapp.log',filemode='a')

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
