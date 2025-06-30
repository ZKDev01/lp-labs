from contracts import (
  contract, 
  catch_contract_errors, catch_errors, 
  _validate_ensure_signature, _validate_require_signature,
  ContractError, PostconditionError, PreconditionError, ContractSignatureError, 
)

def test1() -> None:
  # ejemplo básico
  @catch_contract_errors
  @contract(require=lambda x: x > 0, ensure=lambda result: result > 0)
  def square_root_approx(x: float) -> float:
    "Aproximación de raíz cuadrada que siempre retorna un valor positivo"
    return x ** 0.5
  
  input_x = float(input("x="))
  result,error_type = square_root_approx(input_x)
  if not result: 
    print(error_type)
  else:
    print(f"square_root_approx({input_x}) = {result}")

def test2() -> None:
  # ejemplo con múltiples parámetros
  @catch_contract_errors
  @contract(
    require=lambda x,y: x > 0 and y > 0,
    ensure=lambda result: result > 0
  )
  def multiply_positive(x: float, y: float) -> float:
    "Multiplica dos números positivos"
    return x * y
  
  input_x = float(input("x="))
  input_y = float(input("y="))
  result,error_type = multiply_positive(input_x, input_y)
  if not result:
    print(error_type)
  else:
    print(f"multiply_positive(3, 4) = {result}")

def test3() -> None:
  @catch_contract_errors
  @contract(
    require=lambda x: isinstance(x, (int, float)),
    ensure=lambda result: abs(result) <= 10  
  )
  def clamp_to_range(x: float) -> float:
    "Limita un valor al rango [-10, 10]"
    return max(-10, min(10, x))
  
  input_x = float(input("x="))
  result,error_type = clamp_to_range(input_x)
  if not result:
    print(error_type)
  else:
    print(f"clamp_to_range({input_x}) = {result}")

def test4() -> None:
  
  def f0(x):  # Bien
    return True
  
  def f1(x,y):  # Mal
    return True
  
  def f2(x, y=0):  # Bien
    return True

  def f3(x, *, y):  # Mal
    return True

  def f4(x, *, y=0):  # Bien
    return True
  
  def f5(x, y, *, z):  # Mal
    return True 
  
  def f6(x, y, *, z=0):  # Mal 
    return True
  
  def f7(x, y=0, *, z):  # Mal
    return True
  
  def f8(x, y=0, *, z=0):  # Bien
    return True

  valid_functions = [f0, f2, f4, f8] 
  invalid_functions = [f1, f3, f5, f6, f7]
  
  for func in valid_functions:
    try:
      _validate_ensure_signature(func)
      print(f"{func.__name__}: Válida")
    except ContractSignatureError as e:
      print(f"{func.__name__}: Inválida - {e}")
  
  for func in invalid_functions:
    try:
      _validate_ensure_signature(func)
      print(f"{func.__name__}: Válida (¿ERROR?)")
    except ContractSignatureError as e:
      print(f"{func.__name__}: Inválida correctamente - {e}")



# Ejemplos de uso y pruebas
if __name__ == "__main__":
  #test1()
  #test2()
  #test3()
  test4()
  
