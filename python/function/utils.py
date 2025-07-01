import random 
from enum import Enum
from typing import Generator, List


class Profession(Enum):
  ENGINEER  = "Engineer"
  DOCTOR    = "Doctor"
  TEACHER   = "Teacher"
  ARTIST    = "Artist"
  CHEF      = "Chef"
  LAWYER    = "Lawyer"
  NURSE     = "Nurse"
  ARCHITECT = "Architect"
  WRITER    = "Writer"
  MECHANIC  = "Mechanic"

class Person:
  "Clase para representar una persona con nombre y profesión"
  
  def __init__(self, name:str, age:int, profession:Profession):
    self.name:str = name
    self.age:int = age
    self.profession:Profession = profession
  
  def __str__(self):
    return f"Person(name='{self.name}', age={self.age}, profession='{self.profession.value}')"
  
  def __repr__(self):
    return self.__str__()


def create_person_generator(names_list:List[str], n:int) -> Generator:
  for _ in range(n):
    name = random.choice(names_list)
    age = random.randint(10, 40)
    profession:Profession = random.choice(list(Profession))
    yield Person(name,age,profession)


if __name__ == "__main__":
  names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona"]
  for person in create_person_generator(names, 3):
    print(person)