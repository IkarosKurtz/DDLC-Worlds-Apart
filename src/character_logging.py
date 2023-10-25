from character_data import CharacterDetails

import logging

class CustomLogger:
    LOG_FORMAT = '[%(levelname)s]: %(message)s - %(asctime)s'
    DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, personal_data: CharacterDetails) -> None:
        self._agent_logger = self._setup_logger(f'{personal_data.name}_char', f'logs/{personal_data.name}_char.log')
        self._memory_logger = self._setup_logger(f'{personal_data.name}_mem', f'logs/{personal_data.name}_mem.log')

    def _setup_logger(self, name: str, log_file: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        console_handler = self._create_handler(logging.StreamHandler(), logging.WARNING)
        file_handler = self._create_handler(logging.FileHandler(log_file), logging.INFO)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger

    def _create_handler(self, handler: logging.Handler, level: int) -> logging.Handler:
        handler.setLevel(level)
        formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.DATE_FORMAT)
        handler.setFormatter(formatter)
        return handler

    def agent_info(self, message: str) -> None:
        self._agent_logger.info(message)

    def agent_warning(self, message: str) -> None:
        self._agent_logger.warning(message)

    def agent_error(self, message: str) -> None:
        self._agent_logger.error(message)

    def agent_critical(self, message: str) -> None:
        self._agent_logger.critical(message)

    def memory_info(self, message: str) -> None:
        self._memory_logger.info(message)

    def memory_warning(self, message: str) -> None:
        self._memory_logger.warning(message)

    def memory_error(self, message: str) -> None:
        self._memory_logger.error(message)

    def memory_critical(self, message: str) -> None:
        self._memory_logger.critical(message)
