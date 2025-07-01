import gc
import weakref

# Ejemplo 1: Referencias circulares y garbage collection
print("1. Referencias circulares y garbage collection:")
print("-"*30)

class Node:
  def __init__(self, value):
    self.value = value
    self.parent = None
    self.children = []
    
  def add_child(self, child):
    child.parent = self
    self.children.append(child)
    
  def __del__(self):
    print(f"Node {self.value} eliminado")

# Deshabilitamos temporalmente el garbage collector para demostrar el problema
gc.disable()

# Creamos una estructura con referencias circulares
root = Node("root")
child1 = Node("child1")
child2 = Node("child2")

root.add_child(child1)
root.add_child(child2)

print("Estructura creada con referencias circulares")
print(f"Objetos en memoria antes de eliminar referencias: {len(gc.get_objects())}")

# Eliminamos la referencia principal
del root, child1, child2

print("Referencias eliminadas - objetos permanecen por referencia circular")
print("Los objetos Node no se eliminan automáticamente")

# Habilitamos el garbage collector y lo ejecutamos manualmente
print("Ejecutando garbage collection manualmente...")
gc.enable()
collected = gc.collect()
print(f"Objetos recolectados por garbage collection: {collected}")

# Ejemplo 2: Ejemplo práctico del módulo gc
print("-"*30)
print("2. Ejemplo práctico del módulo gc:")
print("-"*30)

# Información sobre el garbage collector
print(f"Generaciones del GC: {gc.get_count()}")
print(f"Umbrales del GC: {gc.get_threshold()}")

# Creamos objetos que formarán ciclos
class Container:
  def __init__(self, name):
    self.name = name
    self.ref = None
    
  def __repr__(self):
    return f"Container({self.name})"

# Creamos contenedores con referencias circulares
containers = []
for i in range(5):
  c1 = Container(f"A{i}")
  c2 = Container(f"B{i}")
  c1.ref = c2
  c2.ref = c1
  containers.append((c1, c2))

print(f"Objetos creados. Total en memoria: {len(gc.get_objects())}")

# Configuramos callbacks para el garbage collector
def gc_callback(phase, info):
    print(f"GC callback: fase={phase}, info={info}")

# Registramos el callback (solo en Python 3.3+)
try:
  gc.callbacks.append(gc_callback)
except AttributeError:
  print("Callbacks no disponibles en esta versión de Python")

# Eliminamos las referencias y forzamos garbage collection
del containers
print("Forzando garbage collection...")
collected = gc.collect()
print(f"Objetos recolectados: {collected}")

# Ejemplo 3: Detectar y manejar referencias circulares
print("-" * 30)
print("3. Detectar referencias circulares:")
print("-" * 30)

# Creamos objetos con referencias circulares
obj1 = {}
obj2 = {}
obj1['ref'] = obj2
obj2['ref'] = obj1

# Detectamos objetos no alcanzables
print("Buscando objetos no alcanzables...")
unreachable = gc.collect()
print(f"Objetos no alcanzables encontrados: {unreachable}")

# Obtenemos estadísticas del garbage collector
print(f"Estadísticas del GC: {gc.get_stats()}")

# Ejemplo 4: Weak references para evitar ciclos
print("-" * 30)
print("4. Weak references para evitar ciclos:")
print("-" * 30)

class Parent:
  def __init__(self, name):
    self.name = name
    self.children = []
    
  def add_child(self, child):
    self.children.append(child)
    # Usamos weak reference para evitar ciclo
    child.parent = weakref.ref(self)
    
  def __del__(self):
    print(f"Parent {self.name} eliminado")

class Child:
  def __init__(self, name):
    self.name = name
    self.parent = None
    
  def get_parent(self):
    if self.parent is not None:
      return self.parent()  # Llamamos a la weak reference
    return None
    
  def __del__(self):
    print(f"Child {self.name} eliminado")

# Creamos la relación padre-hijo con weak references
parent = Parent("Papa")
child = Child("Hijo")
parent.add_child(child)

print(f"Padre del hijo: {child.get_parent().name}")

# Al eliminar el padre, no hay ciclo que impida la eliminación
del parent
print("Padre eliminado - no hay referencias circulares")

# Forzamos garbage collection para limpiar
gc.collect()

# Configuración del garbage collector
print(f"GC habilitado: {gc.isenabled()}")
print(f"Contadores actuales: {gc.get_count()}")
print(f"Umbrales: {gc.get_threshold()}")

# Configuramos nuevos umbrales
gc.set_threshold(700, 10, 10)
print(f"Nuevos umbrales: {gc.get_threshold()}")

# Restauramos umbrales por defecto
gc.set_threshold(700, 10, 10)
