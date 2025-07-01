import time

# importar decoradores
from utils import (
  measure_time,   # Decorador para medir el tiempo
  handle_errors,  # Decorador para controlar errores en funciones
  
  times,   
  delay,   
  rescue  
)


# Ejemplo: Medir tiempo de una función
@measure_time
def slow_operation(n:int=2) -> None:
  """Simular operación lenta

  Args:
      n (int, optional): tiempo en segundos para simular una tarea. Defaults to 2.
  """
  time.sleep(n)

# Ejemplo: Medir tiempo de una función recursiva
@measure_time
def slow_factorial(n:int) -> int:
  if n < 0: return -1
  return aux_factorial(n)  

def aux_factorial(n:int) -> int:
  slow_operation()
  if n == 1 or n == 0: return 1 
  return n*aux_factorial(n-1)

# Ejemplo: Manejar errores en funciones
@handle_errors
def division(a:float, b:float) -> float:
  "Función que puede manejar errores de división por cero" 
  return a / b


# Ejemplos de TIMES, DELAY y RESCUE
@times 
def show_message(message:str):
  return f"> MESSAGE: {message}"

@measure_time
@delay(1000)
def slow_square(x:int) -> int:
  "Función que calcula el cuadrado de un número con un retraso de 1 segundo"
  return x**2

@rescue(lambda a,b: abs(a) + abs(b))
def positive_sum(a:int, b:int) -> int:
  if a < 0 or b < 0: raise ValueError("Los números no son positivos")
  return a + b 

@times 
@delay(2000)
@rescue(lambda x: f"RESCUE: valor por defecto para {x}")
def complex_function(value: str) -> str:
  "Función con múltiples decoradores"
  if len(value) < 3:
    raise ValueError("El valor debe tener al menos 3 caracteres")
  return f"Procesando: {value.upper()}"


if __name__ == "__main__":
  #slow_operation()
  #print(slow_factorial(4))
  #result = slow_square(10)
  #print(result)
  
  show_message("hola")
  show_message("hola de nuevo")
    
  n = "A"
  for i in range(10):
    value = n*i 
    result = complex_function(value)
    print(f"Resultado de la Función: {result}")
  