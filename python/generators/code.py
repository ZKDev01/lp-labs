
def generator_1():
  yield 1
  yield 2

def generator_2():
  yield 3
  yield 4

def generator_3():
  yield from generator_1()
  print("Generador 1 completado")
  yield from generator_2()
  print("Generador 2 completado")
  return "Generador combinado completado"

generator = generator_3()
while True:
  try:
    print(next(generator))
  except StopIteration as e:
    print(e.value)
    break
