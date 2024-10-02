# logger_config.py
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler

def get_logger(logger_name : str):

    appinsight_connectionstring = os.getenv("AZURE_APPINSIGHT_CONNECTIONSTRING")

    # Crea un logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Configura Azure Log Handler
    log_handler = AzureLogHandler(connection_string=appinsight_connectionstring)
    logger.addHandler(log_handler)

    # Configura Azure Event Handler (opzionale)
    event_handler = AzureEventHandler(connection_string=appinsight_connectionstring)
    logger.addHandler(event_handler)

    return logger