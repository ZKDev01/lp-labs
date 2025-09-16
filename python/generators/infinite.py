def infinite_sequence():
  "A generator that yields an infinite sequence of numbers."
  n = 0
  while True:
    yield n
    n += 1

def square_numbers(sequence):
  "A generator that yields the squares of numbers from an infinite sequence."
  for n in sequence:
    yield n * n

def filter_evens(sequence):
  "A generator that filters even numbers from an infinite sequence."
  for n in sequence:
    if n % 2 == 0:
      yield n

def main():
  # Create an infinite sequence
  infinite_gen = infinite_sequence()

  # Create a generator for squares of numbers
  squares_gen = square_numbers(infinite_gen)

  # Filter even squares
  even_squares_gen = filter_evens(squares_gen)

  # Print the first 10 even squares
  for _ in range(10):
    x = next(even_squares_gen)
    if next(even_squares_gen) > 100:
      print("Infinite generator closed.") 
      infinite_gen.close()
      break
    else: print(x)
    
  #print(next(infinite_gen)) #StopIteration error
  
  # also StopIteration error
  #print(next(squares_gen))

if __name__ == "__main__":  
  main()
