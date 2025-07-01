import time 
from typing import Callable
from functools import wraps



def measure_time(func: Callable) -> Callable:
  """Decorador que mide el tiempo de ejecución de una función. 
  Cuando termina la ejecución de la función se devuelve un diccionario con: resultado de la función y tiempo de ejecución de la misma 
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time 
    return {
      "result": result,
      "time": str(elapsed_time)
    }
  return wrapper

def handle_errors(func: Callable) -> Callable:
  """Decorador que maneja errores y devuelve un diccionario con el resultado y el error.
  
  - Si no hay errores: `{ 'result': value, 'error': None }`
  - Si hay errores: `{ 'result': None, 'error': str(excepcion) }`
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return {
        "result": result,
        "error": None
      }
    except Exception as e:
      return {
        "result": None,
        "error": str(e)
      }  
  return wrapper

def times(func: Callable) -> Callable:
  """Decorador que cuenta el número de veces que se ejecuta una función.
  Almacena el contador como atributo de la función decorada.  
  """
  # inicializar el contador
  func.call_count = 0 
  
  @wraps(func)
  def wrapper(*args, **kwargs):
    # incrementar el contador cada vez que se llama la función
    func.call_count += 1
    print(f"Llamadas a {func.__name__} hechas: {func.call_count}")
    return func(*args, **kwargs)
  
  return wrapper

def delay(milliseconds:int) -> Callable:
  """Decorador que retarda la ejecución de una función por la cantidad especificada de milisegundos

  Args:
      milliseconds (int): cantidad de milisegundos a esperar antes de ejecutar la función
  """
  def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
      # convertir milisegundos a segundos y esperar 
      time.sleep(milliseconds / 1000.0)
      return func(*args, **kwargs)
    return wrapper
  return decorator

def rescue(rescue_func: Callable) -> Callable:
  """Decorador que ejecuta una función alternativa si la función original lanza una excepción

  Args:
      rescue_func (Callable): Función alternativa a ejecutar en caso de excepción
  """
  def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except:
        return rescue_func(*args, **kwargs)
    return wrapper
  return decorator
