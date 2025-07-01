
class A:
  def __init__(self):
    pass

class B:
  def __init__(self,x):
    self.x = x
  
b1 = B(1)
b2 = B(1)
print(id(b1))
print(id(b2))
b1 = B(2)
print(id(b1))
b1 = B(1)
print(id(b1))

""" 
a1 = A()
a2 = A()

id_a1 = id(a1)
id_a2 = id(a2)

print(id_a1 == id_a2)
print(id_a1)
print(id_a2)

b1 = B("b")
b2 = B("b")
b3 = B(1)
b4 = B(1)

id_b1 = id(b1)
id_b2 = id(b2)

print(id_b1 == id_b2)
print(id_b1)
print(id_b2)

id_b3 = id(b3)
id_b4 = id(b4)


print(id_b3 == id_b4)
print(id_b3)
print(id_b4)
"""