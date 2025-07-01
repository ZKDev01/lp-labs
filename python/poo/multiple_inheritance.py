class Person:
  "Clase base que representa una persona"
    
  def __init__(self, name: str, age: int, **kwargs) -> None:
    """Inicializa una persona con nombre y edad.
    
    Args:
      name: Nombre de la persona
      age: Edad de la persona
    """
    self.name: str = name
    self.age: int = age
    
  def action(self):
    "Método base para acciones. Debe ser sobrescrito en clases derivadas"
    print("I am a person")
    
  def __str__(self) -> str:
    "Representación en cadena de la persona"
    return f'{self.name} {self.age}'




class Student(Person):
  "Clase que representa un estudiante, hereda de `Person`"
    
  def __init__(self, name: str, age: int, student_id: int, **kwargs) -> None:
    """Inicializa un estudiante.
    
    Args:
      name: Nombre del estudiante
      age: Edad del estudiante
      student_id: ID único del estudiante
    """
    super().__init__(name, age, **kwargs)
    self.student_id: int = student_id
    
  def __str__(self) -> str:
    "Representación en cadena del estudiante"
    return f'{self.name} {self.age} ID:{self.student_id}'
    
  def action(self):
    "Acción específica del estudiante"
    print("I study")
    
  def study_subject(self, subject: str):
    "Método específico para estudiar una materia"
    print(f"I am studying {subject}")


class Teacher(Person):
  "Clase que representa un profesor, hereda de `Person`"
    
  def __init__(self, name: str, age: int, subject: str, **kwargs) -> None:
    """Inicializa un profesor
        
    Args:
      name: Nombre del profesor
      age: Edad del profesor
      subject: Materia que enseña
    """
    super().__init__(name, age, **kwargs)
    self.subject:str = subject
    
  def __str__(self) -> str:
    "Representación en cadena del profesor"
    return f'{self.name} {self.age} teaches {self.subject}'
    
  def action(self):
    "Acción específica del profesor"
    print("I teach")
    
  def teach_subject(self):
    "Método específico para enseñar la materia"
    print(f"I am teaching {self.subject}")


class StudentTeacher(Student, Teacher):
  """
  Clase que representa a alguien que es tanto estudiante como profesor.
  Utiliza herencia múltiple de `Student` y `Teacher`.
  """
    
  def __init__(self, name: str, age: int, student_id: int, subject: str) -> None:
    """
    Inicializa un estudiante-profesor usando super() y pasando todos los argumentos.
    
    Args:
      name: Nombre
      age: Edad
      student_id: ID de estudiante
      subject: Materia que enseña
    """
    super().__init__(name=name, age=age, student_id=student_id, subject=subject)
    
  def __str__(self) -> str:
    "Representación en cadena del estudiante-profesor"
    return f'{self.name} {self.age} ID:{self.student_id} teaches {self.subject}'
    
  def action(self):
    """
    Acción combinada del estudiante-profesor.
    Resuelve la ambigüedad llamando explícitamente a ambos métodos.
    """
    print("As a student-teacher, I both study and teach")
    # Se llama explícitamente a los métodos de ambas clases padre
    Student.action(self)
    Teacher.action(self)
    
  def daily_routine(self):
    "Rutina diaria específica del estudiante-profesor"
    print(f"Morning: I study as student ID {self.student_id}")
    print(f"Afternoon: I teach {self.subject}")

class StudentTeacherComposition:
  """
  Clase que representa a alguien que es tanto estudiante como profesor.
  Versión alternativa usando composición en lugar de herencia múltiple
  """
  
  def __init__(self, name: str, age: int, student_id: int, subject: str) -> None:
    """
    Inicializa usando composición en lugar de herencia.
        
    Args:
      name: Nombre
      age: Edad  
      student_id: ID de estudiante
      subject: Materia que enseña
    """
    # Creamos instancias separadas de Student y Teacher
    self.student_role = Student(name, age, student_id)
    self.teacher_role = Teacher(name, age, subject)
    
  def __str__(self) -> str:
    "Representación en cadena combinando ambos roles"
    return f'{self.student_role.name} {self.student_role.age} ID:{self.student_role.student_id} teaches {self.teacher_role.subject}'
    
  def action(self):
    "Acción que combina ambos roles"
    print("As a student-teacher:")
    self.student_role.action()
    self.teacher_role.action()
  
  def study_subject(self, subject: str):
    "Delega la acción de estudiar al rol de estudiante"
    self.student_role.study_subject(subject)
    
  def teach_subject(self):
    "Delega la acción de enseñar al rol de profesor"
    self.teacher_role.teach_subject()


if __name__ == "__main__":
  # Crear instancias de cada tipo
  person = Person("Ana", 30)
  student = Student("Carlos", 20, 12345)
  teacher = Teacher("María", 35, "Mathematics")
    
  # Herencia múltiple
  student_teacher = StudentTeacher("Luis", 28, 67890, "Physics")
    
  # Composición
  student_teacher_comp = StudentTeacherComposition("Sofia", 26, 54321, "Chemistry")
    
  print("=== Ejemplos de uso ===")
  print("Person:", person)
  print("Student:", student)
  print("Teacher:", teacher)
  print("StudentTeacher (herencia):", student_teacher)
  print("StudentTeacher (composición):", student_teacher_comp)
    
  print("=== Acciones ===")
  person.action()
  student.action()
  teacher.action()
  print("=== StudentTeacher con herencia múltiple ===")
  student_teacher.action()
  print("=== StudentTeacher con composición ===")
  student_teacher_comp.action()
  print("=== MRO (Method Resolution Order) ===")
  print("StudentTeacher MRO:", [c.__name__ for c in StudentTeacher.mro()])