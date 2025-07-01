

from types import SimpleNamespace

obj1 = SimpleNamespace()
obj1.x = 10
tmp = obj1.x

def square(simple_obj):
  print(id(simple_obj))
  print(id(simple_obj.x))
  print("------------------")
  simple_obj.x = simple_obj.x * simple_obj.x
  print(id(simple_obj))
  print(id(simple_obj.x))


print(id(obj1))
print(id(obj1.x))
print("===========")
square(obj1)
print("===========")
print(id(obj1))
print(id(obj1.x))
print(id(tmp))


