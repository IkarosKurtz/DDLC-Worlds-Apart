from concurrent.futures import ThreadPoolExecutor
from functools import wraps

def create_thread(executor=None):
  def decorator(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      with (executor or ThreadPoolExecutor()) as ex:
        return ex.submit(f, *args, **kwargs)
    
    return wrap

  return decorator
