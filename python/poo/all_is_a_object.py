def foo():
  pass

print( isinstance( 1, object ) )       # True
print( isinstance( list(), object ) )  # True
print( isinstance( True, object ) )    # True
print( isinstance( foo, object ) )     # True
print( isinstance( foo(), object ) )   # True
