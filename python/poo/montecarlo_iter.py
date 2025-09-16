import random

N = 10
LIMIT = 1000

class MonteCarloIterator:
  def __init__(self,n):
    self.n = n 
    self.items = []
  
  def get_list(self):
    return self.items
  
  def __iter__(self):
    return self

  def __next__(self):
    value = random.randint(1, self.n) 
    self.items.append(value)
    return value 

random_number_generator = MonteCarloIterator(LIMIT)
for random_number in random_number_generator:
  print(random_number)
  if len(random_number_generator.get_list()) >= N:
    break

print("Generated numbers:", random_number_generator.get_list()) 