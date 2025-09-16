
def my_generator():
  n = 1
  yield n

def my_range(N):
  n = 0
  while n < N:
    yield n
    n += 1

def test_1() -> None:
  g = my_generator()
  print (type(g)) # <class 'generator'>
  print (next(g)) # 1
  #print (next(g)) # StopIteration
  print (g)       # <generator object my_generator at 0x7f8c3c0b2a50>
  print (list(g)) # []
  #print (next(g)) # StopIteration
  print (g)       # <generator object my_generator at 0x7f8c3c0b2a50>

def test_2() -> None:
  g = my_range(5)
  print (type(g)) # <class 'generator'>
  print (next(g)) # 0
  print (next(g)) # 1
  print (next(g)) # 2
  print (next(g)) # 3
  print (next(g)) # 4
  #print (next(g)) # StopIteration
  print (g)       # <generator object my_range at 0x7f8c3c0b2a50>}



class SquareClass:
  def __init__(self,n):
    self.N = n
    self.i = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self.i > self.N:
      raise StopIteration

    result = self.i ** 2
    self.i += 1
    return result

def test_3() -> None:
  g = SquareClass(10)
  print (type(g)) # <class '__main__.SquareClass'>
  print (next(g)) # 0
  print (next(g)) # 1
  print (next(g)) # 4
  print (next(g)) # 9
  print (next(g)) # 16
  while True:
    try:
      print (next(g)) # 25, ... 
    except StopIteration:
      break
  print (g)       # <__main__.SquareClass object at 0x7f8c3c0b2a50>


def test_4():
  gsquare = ( x**2 for x in range(10) )
  print(next(gsquare))    # output: 0
  print(next(gsquare))    # output: 1
  print(next(gsquare))    # output: 4
  
  print(type(gsquare))    # <class 'generator'>



if __name__ == "__main__":
  #test_1()
  #test_2()
  test_3()
  #test_4()