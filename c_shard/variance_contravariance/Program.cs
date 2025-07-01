using System;
using System.Collections.Generic;

// Clases de ejemplo para demostrar herencia
public class Animal
{
  public string Name { get; set; }
  public virtual void MakeSound() => Console.WriteLine("Sonido generico de animal");
}

public class Dog : Animal
{
  public override void MakeSound() => Console.WriteLine("Guau guau");
}

public class Cat : Animal
{
  public override void MakeSound() => Console.WriteLine("Miau miau");
}

// ========== COVARIANZA ==========
// La covarianza permite usar un tipo más derivado donde se espera un tipo base
// Se usa la palabra clave 'out' en interfaces genéricas

public interface IProducer<out T>
{
  T GetItem();
}

public class AnimalProducer<T> : IProducer<T> where T : Animal, new()
{
  public T GetItem() => new T();
}

// ========== CONTRAVARIANZA ==========
// La contravarianza permite usar un tipo base donde se espera un tipo derivado
// Se usa la palabra clave 'in' en interfaces genéricas

public interface IConsumer<in T>
{
  void ProcessItem(T item);
}

public class AnimalProcessor : IConsumer<Animal>
{
  public void ProcessItem(Animal animal)
  {
    Console.WriteLine($"Procesando: {animal.Name}");
    animal.MakeSound();
  }
}

// ========== PROGRAMA PRINCIPAL ==========
class Program
{
  static void Main()
  {
    Console.WriteLine("=== EJEMPLOS DE VARIANZA EN C# ===\n");
    
    // EJEMPLO 1: COVARIANZA CON INTERFACES
    Console.WriteLine("1. COVARIANZA - Interfaces (out):");
    Console.WriteLine("   Podemos asignar IProducer<Dog> a IProducer<Animal>");
    
    IProducer<Dog> dogProducer = new AnimalProducer<Dog>();
    IProducer<Animal> animalProducer = dogProducer; // Covarianza permitida
    
    Animal animal = animalProducer.GetItem();
    animal.Name = "Rex";
    animal.MakeSound();
    Console.WriteLine();

    // EJEMPLO 2: COVARIANZA CON ARRAYS
    Console.WriteLine("2. COVARIANZA - Arrays:");
    Console.WriteLine("   Los arrays son covariantes por defecto");
    
    Dog[] dogs = { new Dog { Name = "Buddy" }, new Dog { Name = "Max" } };
    Animal[] animals = dogs; // Covarianza con arrays
    
    foreach (Animal a in animals)
    {
      Console.WriteLine($"   Animal: {a.Name}");
      a.MakeSound();
    }
    Console.WriteLine();

    // EJEMPLO 3: CONTRAVARIANZA
    Console.WriteLine("3. CONTRAVARIANZA - Interfaces (in):");
    Console.WriteLine("   Podemos asignar IConsumer<Animal> a IConsumer<Dog>");
    
    IConsumer<Animal> animalConsumer = new AnimalProcessor();
    IConsumer<Dog> dogConsumer = animalConsumer; // Contravarianza permitida
    
    Dog myDog = new Dog { Name = "Luna" };
    dogConsumer.ProcessItem(myDog);
    Console.WriteLine();

    // EJEMPLO 4: COVARIANZA CON DELEGATES
    Console.WriteLine("4. COVARIANZA - Delegates:");
    Console.WriteLine("   Los delegates de retorno son covariantes");
    
    Func<Dog> getDog = () => new Dog { Name = "Thor" };
    Func<Animal> getAnimal = getDog; // Covarianza con delegates
    
    Animal result = getAnimal();
    result.MakeSound();
    Console.WriteLine();

    // EJEMPLO 5: CONTRAVARIANZA CON DELEGATES
    Console.WriteLine("5. CONTRAVARIANZA - Delegates:");
    Console.WriteLine("   Los delegates de parámetros son contravariantes");
    
    Action<Animal> processAnimal = (a) => {
      Console.WriteLine($"   Procesando animal: {a.Name}");
      a.MakeSound();
    };
    
    Action<Dog> processDog = processAnimal; // Contravarianza con delegates
    Dog testDog = new Dog { Name = "Rocco" };
    processDog(testDog);
    Console.WriteLine();

    // EJEMPLO 6: COVARIANZA CON IENUMERABLE
    Console.WriteLine("6. COVARIANZA - IEnumerable<T>:");
    Console.WriteLine("   IEnumerable es covariante (out T)");
    
    List<Cat> cats = new List<Cat> 
    { 
      new Cat { Name = "Whiskers" }, 
      new Cat { Name = "Shadow" } 
    };
    
    IEnumerable<Animal> animalEnum = cats; // Covarianza
    
    foreach (Animal cat in animalEnum)
    {
      Console.WriteLine($"   Gato: {cat.Name}");
      cat.MakeSound();
    }

    Console.WriteLine("\nPresiona cualquier tecla para salir...");
    Console.ReadKey();
  }
}