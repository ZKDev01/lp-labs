using System;
using System.Collections.Generic;

// Interfaz base para los productos
public interface IProduct
{
  void Display();
  string GetInfo();
}

// Productos concretos
public class Laptop : IProduct
{
  public string Brand { get; set; }
  public int Ram { get; set; }
  public string Processor { get; set; }

  public void Display()
  {
    Console.WriteLine($"Laptop: {Brand} - RAM: {Ram}GB - Procesador: {Processor}");
  }

  public string GetInfo()
  {
    return $"Laptop {Brand} con {Ram}GB RAM";
  }
}

public class Smartphone : IProduct
{
  public string Model { get; set; }
  public string Os { get; set; }
  public int Storage { get; set; }

  public void Display()
  {
    Console.WriteLine($"Smartphone: {Model} - SO: {Os} - Almacenamiento: {Storage}GB");
  }

  public string GetInfo()
  {
    return $"Smartphone {Model} con {Os}";
  }
}

public class Tablet : IProduct
{
  public string Brand { get; set; }
  public double ScreenSize { get; set; }
  public bool HasKeyboard { get; set; }

  public void Display()
  {
    Console.WriteLine($"Tablet: {Brand} - Pantalla: {ScreenSize}\" - Teclado: {(HasKeyboard ? "Si" : "No")}");
  }

  public string GetInfo()
  {
    return $"Tablet {Brand} de {ScreenSize} pulgadas";
  }
}

// Factory que utiliza dynamic para crear productos
public class Factory
{
  // Diccionario para mapear tipos de productos
  private static readonly Dictionary<string, Type> ProductTypes = new Dictionary<string, Type>
  {
    { "laptop", typeof(Laptop) },
    { "smartphone", typeof(Smartphone) },
    { "tablet", typeof(Tablet) }
  };

  // Método que crea productos usando dynamic
  public static dynamic CreateProduct(string productType, dynamic parameters = null)
  {
    // Validar si el tipo de producto existe
    if (!ProductTypes.ContainsKey(productType.ToLower()))
    {
      Console.WriteLine($"Tipo de producto '{productType}' no reconocido");
      return null;
    }

    // Crear instancia del tipo solicitado
    Type type = ProductTypes[productType.ToLower()];
    dynamic product = Activator.CreateInstance(type);

    // Configurar propiedades usando dynamic si se proporcionan parámetros
    if (parameters != null)
    {
      ConfigureProduct(product, parameters, productType.ToLower());
    }

    return product;
  }

  // Método privado para configurar las propiedades del producto
  private static void ConfigureProduct(dynamic product, dynamic parameters, string productType)
  {
    try
    {
      switch (productType)
      {
        case "laptop":
          if (HasProperty(parameters, "brand")) product.Brand = parameters.brand;
          if (HasProperty(parameters, "ram")) product.Ram = parameters.ram;
          if (HasProperty(parameters, "processor")) product.Processor = parameters.processor;
          break;

        case "smartphone":
          if (HasProperty(parameters, "model")) product.Model = parameters.model;
          if (HasProperty(parameters, "os")) product.Os = parameters.os;
          if (HasProperty(parameters, "storage")) product.Storage = parameters.storage;
          break;

        case "tablet":
          if (HasProperty(parameters, "brand")) product.Brand = parameters.brand;
          if (HasProperty(parameters, "screenSize")) product.ScreenSize = parameters.screenSize;
          if (HasProperty(parameters, "hasKeyboard")) product.HasKeyboard = parameters.hasKeyboard;
          break;
      }
    }
    catch (Exception ex)
    {
      Console.WriteLine($"Error configurando producto: {ex.Message}");
    }
  }

  // Método auxiliar para verificar si un objeto dynamic tiene una propiedad
  private static bool HasProperty(dynamic obj, string propertyName)
  {
    try
    {
      var value = obj.GetType().GetProperty(propertyName)?.GetValue(obj);
      return true;
    }
    catch
    {
      return false;
    }
  }

  // Método que demuestra el uso de dynamic para operaciones genéricas
  public static void ProcessProduct(dynamic product)
  {
    if (product == null)
    {
      Console.WriteLine("Producto no válido");
      return;
    }

    // Llamar métodos usando dynamic
    Console.WriteLine("=== Procesando Producto ===");
    product.Display();
    
    // Obtener información usando dynamic
    string info = product.GetInfo();
    Console.WriteLine($"Información: {info}");

    // Acceso dinámico a propiedades específicas según el tipo
    Console.WriteLine("=== Propiedades Específicas ===");
    ShowProductSpecificInfo(product);
  }

  // Método que muestra información específica usando dynamic
  private static void ShowProductSpecificInfo(dynamic product)
  {
    string typeName = product.GetType().Name;
    
    try
    {
      switch (typeName)
      {
        case "Laptop":
          Console.WriteLine($"Marca: {product.Brand}, RAM: {product.Ram}GB");
          break;
        case "Smartphone":
          Console.WriteLine($"Modelo: {product.Model}, SO: {product.Os}");
          break;
        case "Tablet":
          Console.WriteLine($"Marca: {product.Brand}, Pantalla: {product.ScreenSize}\"");
          break;
      }
    }
    catch (Exception ex)
    {
      Console.WriteLine($"Error accediendo a propiedades: {ex.Message}");
    }
  }
}

// Programa principal para demostrar el uso
class Program
{
  static void Main(string[] args)
  {
    Console.WriteLine("Ejemplo Factory Pattern con Dynamic\n");

    // Crear productos usando objetos anónimos como parámetros dynamic
    Console.WriteLine("1. Creando Laptop:");
    dynamic laptop = Factory.CreateProduct("laptop", new { 
      brand = "Dell", 
      ram = 16, 
      processor = "Intel i7" 
    });
    Factory.ProcessProduct(laptop);

    Console.WriteLine("\n2. Creando Smartphone:");
    dynamic phone = Factory.CreateProduct("smartphone", new { 
      model = "iPhone 15", 
      os = "iOS 17", 
      storage = 256 
    });
    Factory.ProcessProduct(phone);

    Console.WriteLine("\n3. Creando Tablet:");
    dynamic tablet = Factory.CreateProduct("tablet", new { 
      brand = "Samsung", 
      screenSize = 10.5, 
      hasKeyboard = true 
    });
    Factory.ProcessProduct(tablet);

    // Crear producto sin parámetros
    Console.WriteLine("\n4. Creando producto sin parámetros:");
    dynamic emptyLaptop = Factory.CreateProduct("laptop");
    Factory.ProcessProduct(emptyLaptop);

    // Intentar crear producto no válido
    Console.WriteLine("\n5. Intentando crear producto no válido:");
    dynamic invalidProduct = Factory.CreateProduct("desktop");
    Factory.ProcessProduct(invalidProduct);

    // Demostrar flexibilidad de dynamic
    Console.WriteLine("\n6. Uso flexible de dynamic:");
    DemonstrateDynamicFlexibility();

    Console.WriteLine("\nPresiona cualquier tecla para salir...");
    Console.ReadKey();
  }

  // Método adicional para demostrar la flexibilidad de dynamic
  static void DemonstrateDynamicFlexibility()
  {
    // Array de productos dynamic
    dynamic[] products = {
      Factory.CreateProduct("laptop", new { brand = "HP", ram = 8, processor = "AMD Ryzen" }),
      Factory.CreateProduct("smartphone", new { model = "Galaxy S24", os = "Android", storage = 128 }),
      Factory.CreateProduct("tablet", new { brand = "iPad", screenSize = 12.9, hasKeyboard = false })
    };

    Console.WriteLine("Procesando array de productos dynamic:");
    foreach (dynamic product in products)
    {
      if (product != null)
      {
        // Acceso dinámico sin conocer el tipo exacto
        Console.WriteLine($"- {product.GetInfo()}");
      }
    }
  }
}