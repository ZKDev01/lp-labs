from typing import List

def f1(x:List):
  x.append(1000)

def f2():
  a.append(1000) 

a = [1,2,3]
print(a)

""" 
f1(a)
print(a)
"""

f2()
print(a)
