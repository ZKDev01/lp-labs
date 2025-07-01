import random 

class Person:
  def __init__(self, name:str):
    self.__id_random:int = random.randint(0, 10000) 
    self.name:str = name 
  
  def __repr__(self):
    return f"Person(name='{self.name}')"
  
  def print_id(self):
    print(self.__id_random)

def test() -> None:
  p = Person("Daniel")
  print(p)
  # intentar obtener y modificar id
  # print(p.__id_random) # 'Person' object has no attribute '__id_random'
  
  p.print_id()  
  p.__id_random = -1000
  print(p.__id_random)
  p.print_id() # no se modifica (no es -1000)
  

if __name__ == "__main__":
  test()