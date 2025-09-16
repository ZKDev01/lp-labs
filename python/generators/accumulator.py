def accumulator():
  total = 0
  while True:
    value = yield total
    if value is not None:
      total += value

def test_1():
  acc = accumulator()
  next(acc)  # Start the generator
  print(acc.send(1))  # Output: 1
  print(acc.send(2))  # Output: 3
  print(acc.send(3))  # Output: 6
  print(acc.send(None))  # Output: 6 (no change)
  print(acc.send(5))  # Output: 11

if __name__ == "__main__":
  test_1()  