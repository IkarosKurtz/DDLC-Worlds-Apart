from concurrent.futures import ThreadPoolExecutor
from functools import wraps


def threaded(f):
  """ Creates a thread for the given function. """
  @wraps(f)
  def wrapped(*args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
      future = executor.submit(f, *args, **kwargs)
      return future.result()
  return wrapped
