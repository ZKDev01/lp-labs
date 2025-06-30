import inspect
from functools import wraps
from typing import Callable, Any, Optional

class ContractError(Exception):
  "Excepción base para errores de contrato"

class PreconditionError(ContractError):
  "Excepción lanzada cuando falla una precondición"

class PostconditionError(ContractError):
  "Excepción lanzada cuando falla una postcondición"

class ContractSignatureError(ContractError):
  "Excepción lanzada cuando la signatura del contrato es inválida"

#region: Validación de signaturas
def _validate_require_signature(require_func: Callable, decorated_func: Callable) -> None:
  """Valida que la signatura de la función de precondición sea compatible con la función decorada.
  
  Args:
      require_func (Callable): 
      decorated_func (Callable): 

  Raises:
      ContractSignatureError: _description_
      ContractSignatureError: _description_
  """
  require_sig = inspect.signature(require_func)
  decorated_sig = inspect.signature(decorated_func)
    
  # Obtener parámetros de ambas funciones
  require_params = list(require_sig.parameters.values())
  decorated_params = list(decorated_sig.parameters.values())
    
  # Verificar que el número de parámetros sea compatible
  # La función require debe poder recibir todos los argumentos de la función decorada
    
  # Contar parámetros requeridos en ambas funciones
  require_required = sum(1 for p in require_params if 
    p.default == inspect.Parameter.empty and 
    p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD))
  
  decorated_required = sum(1 for p in decorated_params if  
    p.default == inspect.Parameter.empty and 
    p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD))
    
  # La función require no puede requerir más parámetros que la función decorada
  if require_required > decorated_required:
    raise ContractSignatureError(
      f"La función de precondición requiere {require_required} parámetros, "
      f"pero la función decorada solo tiene {decorated_required} parámetros requeridos"
    )
    
  # Verificar compatibilidad más detallada
  try:
    # Intentar bind con argumentos dummy para verificar compatibilidad
    dummy_args = []
    dummy_kwargs = {}
        
    for i, param in enumerate(decorated_params):
      if param.kind == inspect.Parameter.POSITIONAL_ONLY:
        dummy_args.append(f"arg_{i}")
      elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
        dummy_args.append(f"arg_{i}")
      elif param.kind == inspect.Parameter.KEYWORD_ONLY:
        dummy_kwargs[param.name] = f"kwarg_{param.name}"
    
    # Intentar hacer bind con la función require
    require_sig.bind(*dummy_args[:len(require_params)], **dummy_kwargs)
  
  except TypeError as e:
    raise ContractSignatureError(
      f"La signatura de la función de precondición no es compatible "
      f"con la función decorada: {str(e)}"
    )

def _validate_ensure_signature(ensure_func: Callable) -> None:
  """Valida que la signatura de la función de postcondición sea válida. 
  Solo debe tener un parámetro posicional requerido (result) y parámetros opcionales o keyword-only con valores por defecto.
  
  Args:
      ensure_func (Callable): _description_

  Raises:
      ContractSignatureError: _description_
      ContractSignatureError: _description_
  """
  ensure_sig = inspect.signature(ensure_func)
  params = list(ensure_sig.parameters.values())
  
  # Contar parámetros requeridos
  required_positional = 0
  required_keyword_only = 0
  
  for param in params:
    if param.default == inspect.Parameter.empty:
      if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
        required_positional += 1
      elif param.kind == inspect.Parameter.KEYWORD_ONLY:
        required_keyword_only += 1
      elif param.kind == inspect.Parameter.POSITIONAL_ONLY:
        required_positional += 1
    
  # Verificar que no haya más de un parámetro posicional requerido
  if required_positional > 1:
    raise ContractSignatureError(
      f"La función de postcondición no puede tener más de un parámetro "
      f"posicional requerido. Encontrados: {required_positional}"
    )
    
  # Verificar que no haya parámetros keyword-only requeridos
  if required_keyword_only > 0:
    raise ContractSignatureError(
      f"La función de postcondición no puede tener parámetros "
      f"keyword-only requeridos. Encontrados: {required_keyword_only}"
    )
#endregion

#region: Decoradores

def catch_contract_errors(func: Callable):
  """Decorador para capturar errores de contrato y lanzar excepciones específicas.

  Args:
      func (Callable): Función a decorar.
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs), None
    except (ContractError, PreconditionError, PostconditionError, ContractSignatureError) as e:
      #print(f"Error de contrato: {str(e)}")
      return None, e
    except Exception as e:
      #print(f"Error inesperado: {str(e)}")
      return None, e
  return wrapper

def catch_errors(func: Callable):
  """Version genérica del decorador para capturar cualquier excepción.

  Args:
      func (Callable): Función a decorar.
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs), None
    except Exception as e:
      print(f"Error inesperado: {str(e)}")
      return None, e
  return wrapper

def contract(require: Optional[Callable] = None, ensure: Optional[Callable] = None):
  """Decorador que implementa contratos con pre y postcondiciones.
  
  Args:
      require (Optional[Callable], optional): Función que verifica las precondiciones. Defaults to None.
      ensure (Optional[Callable], optional): Función que verifica las postcondiciones. Defaults to None.
  """
  def decorator(func: Callable) -> Callable:
    # Validar signaturas en tiempo de decoración
    if require is not None: _validate_require_signature(require, func)
    
    if ensure is not None: _validate_ensure_signature(ensure)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
      # Verificar precondiciones
      if require is not None:
        try:
          # Obtener la signatura de la función require para hacer bind correcto
          require_sig = inspect.signature(require)
          bound_args = require_sig.bind_partial(*args, **kwargs)
          bound_args.apply_defaults()
          
          if not require(*bound_args.args, **bound_args.kwargs):
            raise PreconditionError("Falló la verificación de precondición")
        except TypeError as e:
          # Si hay error de signatura, intentar con los argumentos disponibles
          try:
            if not require(*args, **kwargs):
              raise PreconditionError("Falló la verificación de precondición")
          except TypeError:
            raise ContractSignatureError(
              f"Error al evaluar precondición: {str(e)}"
            )
        except Exception as e:
          if isinstance(e, (PreconditionError, ContractSignatureError)):
            raise
          raise PreconditionError(f"Error en precondición: {str(e)}")
      
      # Ejecutar la función original
      result = func(*args, **kwargs)
      
      # Verificar postcondiciones
      if ensure is not None:
        try:
          ensure_sig = inspect.signature(ensure)
          # Intentar llamar con solo el resultado
          if len(ensure_sig.parameters) == 1:
            if not ensure(result):
              raise PostconditionError("Falló la verificación de postcondición")
          else:
            # Llamar con resultado y argumentos disponibles
            bound_args = ensure_sig.bind_partial(result, *args, **kwargs)
            bound_args.apply_defaults()
            if not ensure(*bound_args.args, **bound_args.kwargs):
              raise PostconditionError("Falló la verificación de postcondición")
        except TypeError as e:
          raise ContractSignatureError(f"Error al evaluar postcondición: {str(e)}")
        except Exception as e:
          if isinstance(e, (PostconditionError, ContractSignatureError)):
            raise
          raise PostconditionError(f"Error en postcondición: {str(e)}")
      
      return result
    
    return wrapper
  return decorator
#endregion
