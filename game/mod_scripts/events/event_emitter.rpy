init -999 python:
  from typing import Callable

  class EventEmitter:
    def __init__(self):
      self.events: dict[str, list[callable]] = {}

    def on(self, event: str, callback: callable):
      if event not in self.events:
        self.events[event] = []

      self.events[event].append(callback)

    def emit(self, event: str, *args, **kwargs):
      if event not in self.events:
        return

      for callback in self.events[event]:
        callback(*args, **kwargs)