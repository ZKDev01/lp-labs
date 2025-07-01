def test1():
  class A:
    pass 
  class B(A):
    pass 
  class C(A):
    pass
  class D(B,C):
    pass 
  
  classes = [c.__name__ for c in D.mro()]
  print(classes) # D, B, C, A, object

if __name__ == "__main__":
  test_i = int(input("¿Qué prueba desea ejecutar?\n> "))
  
  match test_i: 
    case 1: test1()
    case 2:
      pass 
    
    case _:
      print("prueba no encontrada")
