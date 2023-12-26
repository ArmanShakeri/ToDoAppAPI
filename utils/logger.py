import logging


class Logger:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(logging.DEBUG)

            # Create a file handler
            file_handler = logging.FileHandler('logs/app.log')

            # Create a formatter and add it to the file handler
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            cls._instance.logger.addHandler(file_handler)

        return cls._instance.logger