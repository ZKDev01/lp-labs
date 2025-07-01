import sys

x = 10
y = x
print(sys.getrefcount(x))
del x 
print(sys.getrefcount(x))

