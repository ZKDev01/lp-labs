from typing import Any, List, Callable, Generator, Iterable
from collections import defaultdict

from faker import Faker
from utils import Person, Profession, create_person_generator


#region WHERE
def where(data:Iterable, predicate:Callable[[Any], bool]) -> Generator:
  """Filtra los elementos de una colección basándose en una función predicado
  
  Args:
    data (Iterable): colección de elementos a filtrar
    predicate (Callable): función que toma un elemento y retorna True/False
  """ 
  for item in data:
    if predicate(item): yield item

#endregion

#region GROUP BY
def group_by(data:Iterable, key_func:Callable[[Any], Any]) -> Generator:
  """Agrupa los elementos de una colección basándose en una función clave

  Args:
    data (Iterable): colección de elementos a agrupar
    key_func (Callable[[Any], Any]): función que extrae la clave de agrupación de cada elemento
  """
  groups = defaultdict(list)
  for item in data:
    key = key_func(item)
    groups[key].append(item)
  for key, group in groups.items():
    yield key, group

#endregion

#region AGGREGATE
def aggregate(data: Iterable, group_func:Callable[[Any], Any], agg_func:Callable[[List[Any]], Any]) -> Generator:
  """Agrupa los datos y aplica una función de agregación a cada grupo. 

  Args:
    data (Iterable): colección de elementos a procesar
    group_func (Callable[[Any], Any]): función que extrae la clave de agrupación
    agg_func (Callable[[List[Any]], Any]): función que reduce cada grupo a un valor único
  """
  for key, group in group_by(data, group_func):
    yield key, agg_func(group)
#endregion

#region TEST
def test1(N:int=50):
  "Test: Generación de N nombres únicos con Faker"
  fake = Faker()
  names = [fake.unique.first_name() for _ in range(N)]
  for i,name in enumerate(names):
    print(f"{i+1}) {name}")

def test2(verbose:bool=True) -> List[Person]:
  "Test: Generación de un objeto Person (Persona) con faker"
  N = 100
  
  fake = Faker()
  names = [fake.unique.first_name() for _ in range(N)]
  
  persons = []
  for person in create_person_generator(names, n=int(0.5*N)):
    if verbose: print(person)
    persons.append(person)
  
  return persons

def test3():
  "Test: Where"
  persons = test2(False)
  
  print("======== Adultos (edad > 25) ========")
  for i, adult in enumerate(where(persons, lambda p: p.age > 25)):
    print(f"{i+1}) {adult}")
  
  print("======== Doctores ========")
  for i, doctor in enumerate(where(persons, lambda p: p.profession == Profession.DOCTOR)):
    print(f"{i+1}) {doctor}")

def test4(): 
  "Test: Group By"
  persons = test2(False)
  
  print("======== Agrupación por profesión ========")
  for profession, group in group_by(persons, lambda p: p.profession):
    print(f"{profession.value}: {len(group)} personas")
  
  print("======== Agrupación por rango de edad ========")
  for age_range, group in group_by(persons, lambda p: "Joven" if p.age < 25 else "Adulto"):
    print(f"{age_range}: {len(group)} personas")

def test5():
  "Test: Aggregate"
  persons = test2(False)
  
  print("======== Edad promedio por profesión ========")
  for profession, avg_age in aggregate(persons, 
                    lambda p: p.profession,
                    lambda group: round(sum(p.age for p in group) / len(group), 1)):
    print(f"{profession.value}: {avg_age} años")
  
  print("======== Persona más joven por profesión ========")
  for profession, youngest in aggregate(persons, 
                    lambda p: p.profession, 
                    lambda group: min(group, key=lambda p: p.age)):
    print(f"{profession.value}: {youngest.name} ({youngest.age} años)")

#endregion

#region MAIN
def main() -> None:
  test_i = int(input("¿Qué prueba desea ejecutar?\n> "))
  
  if test_i == 1: test1()
  if test_i == 2: test2()
  if test_i == 3: test3()
  if test_i == 4: test4()
  if test_i == 5: test5()

#endregion

if __name__ == "__main__":
  main()
