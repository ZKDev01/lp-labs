from functools import reduce

filtered = list(filter(lambda x: x > 5, range(1, 10)))
print(filtered)  # [6, 7, 8, 9]

mapped = list(map(lambda x: x * 2, range(1, 6)))
print(mapped)  # [2, 4, 6, 8, 10] 

sum_all = reduce(lambda x, y: x + y, range(1, 6))
print(sum_all)  # 15

factorial = reduce(lambda x, y: x * y, range(1, 6),10)
print(factorial)  # 120

#region examples: map
print("Exmaples: map function")

def square(num:int) -> int:
  return num**2

f = lambda x,y=2 : x**y

N = 10

# Use map function to process list items without using loops
x = [i for i in range(0,N+1)]
s = list(map(f,x))

printer = f"""
x = {x}
s = {s}
"""
print (printer)

#endregion