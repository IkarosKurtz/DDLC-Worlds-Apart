init -999 python:
  import logging
  import os


  class CustomLogger:
    """ A custom logger class for logging messages related to character details and memory. """

    LOG_FORMAT = '[%(levelname)s # %(asctime)s]: %(message)s'
    DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, agent_name: str) -> None:
      """
      Initializes the CustomLogger instance, setting up loggers for both character
      and memory with separate log files.

      Parameters
      ----------
      agent_name : str
        The name of the agent.
      """
      root_dir = os.path.dirname(renpy.config.gamedir)

      if not os.path.exists(f'{root_dir}/logs'):
        os.mkdir(f'{root_dir}/logs')

      if not os.path.exists(f'{root_dir}/logs/{agent_name}'):
        os.mkdir(f'{root_dir}/logs/{agent_name}')

      if os.path.exists(f'{root_dir}/logs/{agent_name}/{agent_name}_char.log'):
        os.remove(f'{root_dir}/logs/{agent_name}/{agent_name}_char.log')

      if os.path.exists(f'{root_dir}/logs/{agent_name}/{agent_name}_memories.log'):
        os.remove(f'{root_dir}/logs/{agent_name}/{agent_name}_memories.log')

      self._agent_logger = self._setup_logger(f'{agent_name}_char', f'{root_dir}/logs/{agent_name}/{agent_name}_char.log')
      self._memory_logger = self._setup_logger(f'{agent_name}_memories', f'{root_dir}/logs/{agent_name}/{agent_name}_memories.log')

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

      logger.propagate = False

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

    def both_info(self, message: str) -> None:
      """Logs an info message in both loggers."""
      self._agent_logger.info(message)
      self._memory_logger.info(message)

    def both_warning(self, message: str) -> None:
      """Logs a warning message in both loggers."""
      self._agent_logger.warning(message)
      self._memory_logger.warning(message)

    def both_error(self, message: str) -> None:
      """Logs an error message in both loggers."""
      self._agent_logger.error(message)
      self._memory_logger.error(message)

    def both_critical(self, message: str) -> None:
      """Logs a critical message in both loggers."""
      self._agent_logger.critical(message)
      self._memory_logger.critical(message)
