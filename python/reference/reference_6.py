
class A:
  def __init__(self,x):
    self.x = x

a = A("a")
print(id(a))
a = A("b")
print(id(a))
a = A("a")
print(id(a))


