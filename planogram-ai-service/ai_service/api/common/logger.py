import logging

def configure_logging(path_log=None):
    log_formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
    root_logger = logging.getLogger()

    # to file
    if path_log:
        file_handler = logging.FileHandler(path_log)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    # std
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    root_logger.setLevel(logging.DEBUG)


