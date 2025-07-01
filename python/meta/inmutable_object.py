class InmutableObject:
  """
  Clase base que implementa objetos inmutables.
  Una vez creada la instancia, no se pueden modificar ni eliminar atributos.
  """
  
  def __init__(self):
    # Se marca el objeto para decir que está en proceso de inicialización
    object.__setattr__(self, '_init', False)
    # Al final de __init__, se marca como inicializado
    object.__setattr__(self, '_init', True)
    
  def __setattr__(self, name, value):
    "Impide la asignación de atributos después de la inicialización"
    # Durante la inicialización, se pueden establecer atributos
    if not hasattr(self, '_init') or not self._init:
      object.__setattr__(self, name, value)
    else:
      raise AttributeError(f"No se puede modificar el atributo '{name}' en un objeto inmutable")
    
  def __delattr__(self, name):
    "Impide la eliminación de atributos"
    raise AttributeError(f"No se puede eliminar el atributo '{name}' en un objeto inmutable")


class Person(InmutableObject):
  def __init__(self, name:str, age:int):
    # Establecer los atributos antes de llamar a super().__init__()
    self.name = name 
    self.age = age 
    # Llamar al constructor padre para marcar como inicializado
    super().__init__()
  
  def __str__(self):
    return f"Person(name='{self.name}', age={self.age})"
    
  def __repr__(self):
    return self.__str__()
  
  def greet(self, message:str):
    return f"Person(name='{self.name}') say: {message}"

if __name__ == "__main__":
  print("=== Pruebas con ObjetoInmutable ===")
  
  # Crear instancias
  p = Person("Daniel", 23)
  
  print(p)
  p.greet("good morning!")
  
  try:
    p.name = "Raimel"
  except AttributeError as e: 
    print(f"Modificación no posible: {e}")
  
  try:
    p.profession = "programmer"
  except AttributeError as e: 
    print(f"Adición no posible: {e}")
  
  try: 
    del p.name 
  except AttributeError as e:
    print(f"Eliminación no posible: {e}")
  
  print(p)