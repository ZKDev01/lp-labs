from functools import reduce

filtered = list(filter(lambda x: x > 5, range(1, 10)))
print(filtered)  # [6, 7, 8, 9]

mapped = list(map(lambda x: x * 2, range(1, 6)))
print(mapped)  # [2, 4, 6, 8, 10] 

sum_all = reduce(lambda x, y: x + y, range(1, 6))
print(sum_all)  # 15

factorial = reduce(lambda x, y: x * y, range(1, 6),10)
print(factorial)  # 120