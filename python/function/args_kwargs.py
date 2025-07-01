def test1(func, *other_args, **other_kwargs):
  func(other_args,other_kwargs)

def test2(*args, func, **kwargs):
  func(args,kwargs)

def test3(func, *other_args, **other_kwargs):
  func(other_args,kwargs=other_kwargs)

def test4(*args, func, **kwargs):
  func(args,kwargs=kwargs)


def f(*args, **kwargs):
  print(*args)
  print(**kwargs)
  print("=========")
  print(args)
  print(kwargs)


if __name__ == "__main__":
  test_i = int(input("¿Qué prueba desea ejecutar?\n> "))
  
  match test_i: 
    case 1: 
      test1(f,1,2,3,x1=4,x2=5,x3=6)
    case 2: 
      test2(f,1,2,3, func=f, x1=4,x2=5,x3=6)
    case 3: 
      test3(f,1,2,3,x1=4,x2=5,x3=6)
    case 4:
      test4(f,1,2,3, func=f, x1=4,x2=5,x3=6)
    case _:
      print("prueba no encontrada")

  
  
  
  

