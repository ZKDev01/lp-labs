class SingletonMeta(type):
  """
  Metaclase que implementa el patrón Singleton.
  Garantiza que solo exista una instancia de cada clase que use esta metaclase
  """
  _instances = { }
  
  def __call__(cls, *args, **kwargs):
    "Controla la creación de instancias"
    if cls not in cls._instances:
      instance = super().__call__(*args, **kwargs)
      cls._instances[cls] = instance
    return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
  """Clase base Singleton. 
  Todas las clases que hereden de esta tendrán comportamiento singleton automático
  """
  pass 

class Logger(Singleton):
  def __init__(self):
    self.logs = []

  def log(self, message):
    self.logs.append(message)

if __name__ == "__main__":
  # Ejemplo de uso
  logger1 = Logger()
  logger2 = Logger()

  logger1.log("Mensaje 1")
  logger2.log("Mensaje 2")

  print(logger1.logs)  # ['Mensaje 1', 'Mensaje 2']
  print(logger1 is logger2)  # True