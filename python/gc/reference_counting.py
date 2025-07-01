import sys

# Ejemplo 1: Reference Counting básico
print("1. Reference Counting básico:")
print("-"*30)

# Creamos un objeto y vemos su reference count
my_list = [1, 2, 3, 4, 5]
print(f"Reference count inicial: {sys.getrefcount(my_list)}")

# Creamos otra referencia al mismo objeto
another_reference = my_list
print(f"Reference count después de crear otra referencia: {sys.getrefcount(my_list)}")

# Eliminamos una referencia
del another_reference
print(f"Reference count después de eliminar una referencia: {sys.getrefcount(my_list)}")

# Ejemplo 2: Reference Counting con estructuras de datos
print("-"*30)
print("2. Reference Counting con estructuras complejas:")
print("-"*30)

class Person:
  def __init__(self, name):
    self.name = name
    self.friends = []
    
  def add_friend(self, friend):
    self.friends.append(friend)
    
  def __del__(self):
    print(f"Objeto {self.name} ha sido eliminado")

# Creamos objetos y vemos como cambia el reference count
alice = Person("Alice")
print(f"Reference count de Alice: {sys.getrefcount(alice)}")

bob = Person("Bob")
print(f"Reference count de Bob: {sys.getrefcount(bob)}")

# Agregamos referencias cruzadas
alice.add_friend(bob)
bob.add_friend(alice)

print(f"Reference count de Alice después de agregar amigo: {sys.getrefcount(alice)}")
print(f"Reference count de Bob después de agregar amigo: {sys.getrefcount(bob)}")

# Eliminamos las referencias principales
del alice
del bob
print("Referencias principales eliminadas - objetos aún pueden existir por referencias circulares")
