
def main():
  n = 5
  print(f"n: {id(n)}")
  increment(n)
  print(f"n: {id(n)}")
  
def increment(x):
  print(f"x: {id(x)}")
  x = x + 1
  print(f"x: {id(x)}")
  
main()

""" 
output:
  n: 140736273074744
  x: 140736273074744  
  x: 140736273074776  
  n: 140736273074744
"""