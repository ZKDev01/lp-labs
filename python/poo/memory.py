
#region CLASES
class Animal: 
  def __init__(self,name:str) -> None:
    self.name:str = name
  
class Perro(Animal):
  def f(self) -> None:
    print ("Guau")
  
class Gato(Animal):
  def f(self) -> None:
    print ("Miau")
#endregion

#region MAIN
def main() -> None:
  animales = [ Perro("p1"), Perro("p2"), Perro("p3") ]
  for animal in animales:
    print(id(animal))
  
  print("===========")
  animales[0] = Gato("g1")
  for animal in animales:
    print(id(animal))
    
  print("===========")
  animales[0] = Perro("p1")
  for animal in animales:
    print(id(animal))

if __name__ == "__main__":
  main()

""" output:
1863740516224
1863740516848
1863740517040
===========
1863740517088
1863740516848
1863740517040
===========
1863740516224
1863740516848
1863740517040
"""
