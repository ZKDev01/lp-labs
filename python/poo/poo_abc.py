from abc import ABC, abstractmethod

class Animal(ABC):  
  @abstractmethod
  def sound(self):
    pass
  
  def sleep(self):
    print("Sleeping...")

class Dog(Animal):
  def sound(self):
    print("Woof! Woof!")

class Cat(Animal):
  pass 

if __name__ == "__main__":
  dog = Dog()
  dog.sound() # Output: Woof! Woof!
  dog.sleep() # Output: Sleeping...
  
  cat = Cat() 
  # TypeError: Can't instantiate abstract class Cat with abstract method sound