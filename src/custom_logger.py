from .character_data import CharacterDetails
import logging
import os


class CustomLogger:
  """ A custom logger class for logging messages related to character details and memory. """

  LOG_FORMAT = '[%(levelname)s # %(asctime)s]: %(message)s'
  DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

  def __init__(self, character_data: CharacterDetails) -> None:
    """
    Initializes the CustomLogger instance, setting up loggers for both character
    and memory with separate log files.

    Parameters
    ----------
    character_data : CharacterDetails
      The character details used to name the loggers and log files.
    """
    if not os.path.exists('logs'):
      os.mkdir('logs')

    self._agent_logger = self._setup_logger(f'{character_data.name}_char', f'logs/{character_data.name}_char.log')
    self._memory_logger = self._setup_logger(f'{character_data.name}_mem', f'logs/{character_data.name}_mem.log')

  def _setup_logger(self, name: str, log_file: str) -> logging.Logger:
    """
    Sets up a logger with the specified name and log file.

    Parameters
    ----------
    name : str
      The name for the logger.
    log_file : str
      The path to the log file.

    Returns
    -------
    logging.Logger
      The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = self._create_handler(logging.StreamHandler(), logging.INFO)
    file_handler = self._create_handler(logging.FileHandler(log_file), logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

  def _create_handler(self, handler: logging.Handler, level: int) -> logging.Handler:
    """
    Creates a log handler with the specified level and formatter.

    Parameters
    ----------
    handler : logging.Handler
      The handler to configure.
    level : int
      The logging level for the handler.

    Returns
    -------
    logging.Handler
      The configured log handler.
    """
    handler.setLevel(level)
    formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.DATE_FORMAT)
    handler.setFormatter(formatter)
    return handler

  def agent_info(self, message: str) -> None:
    """Logs an info message in the agent logger."""
    self._agent_logger.info(message)

  def agent_warning(self, message: str) -> None:
    """Logs a warning message in the agent logger."""
    self._agent_logger.warning(message)

  def agent_error(self, message: str) -> None:
    """Logs an error message in the agent logger."""
    self._agent_logger.error(message)

  def agent_critical(self, message: str) -> None:
    """Logs a critical message in the agent logger."""
    self._agent_logger.critical(message)

  def memory_info(self, message: str) -> None:
    """Logs an info message in the memory logger."""
    self._memory_logger.info(message)

  def memory_warning(self, message: str) -> None:
    """Logs a warning message in the memory logger."""
    self._memory_logger.warning(message)

  def memory_error(self, message: str) -> None:
    """Logs an error message in the memory logger."""
    self._memory_logger.error(message)

  def memory_critical(self, message: str) -> None:
    """Logs a critical message in the memory logger."""
    self._memory_logger.critical(message)
