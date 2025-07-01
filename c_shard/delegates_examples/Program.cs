using System;
using System.Collections.Generic;
using System.Linq;

namespace DelegateExamples
{
  class Program
  {
    // =====================================
    // 1. DELEGADOS BÁSICOS
    // =====================================
    
    // Declaración de un delegado personalizado
    public delegate int MathOperation(int x, int y);
    public delegate void NotificationHandler(string message);
    
    // Métodos que coinciden con la firma del delegado
    public static int Add(int x, int y)
    {
      return x + y;
    }
    
    public static int Multiply(int x, int y)
    {
      return x * y;
    }
    
    public static void SendEmail(string message)
    {
      Console.WriteLine($"Email enviado: {message}");
    }
    
    public static void SendSMS(string message)
    {
      Console.WriteLine($"SMS enviado: {message}");
    }
    
    static void Main(string[] args)
    {
      Console.WriteLine("=== EJEMPLOS DE DELEGADOS EN C# ===\n");
      
      // Ejemplos de delegados básicos
      DelegateBasicExamples();
      
      // Ejemplos de Func<T>
      FuncExamples();
      
      // Ejemplos de Action<T>
      ActionExamples();
      
      // Ejemplos de Predicate<T>
      PredicateExamples();
      
      // Ejemplos de funciones puras
      PureFunctionExamples();
      
      // Ejemplos de funciones de orden superior
      HigherOrderFunctionExamples();
      
      Console.ReadKey();
    }
    
    // =====================================
    // DELEGADOS BÁSICOS
    // =====================================
    static void DelegateBasicExamples()
    {
      Console.WriteLine("--- DELEGADOS BÁSICOS ---");
      
      // Crear instancia del delegado y asignar método
      MathOperation operation = Add;
      int result = operation(5, 3);
      Console.WriteLine($"Suma: {result}");
      
      // Cambiar el método asignado
      operation = Multiply;
      result = operation(5, 3);
      Console.WriteLine($"Multiplicación: {result}");
      
      // Delegado multicast - combinar múltiples métodos
      NotificationHandler notifications = SendEmail;
      notifications += SendSMS; // Agregar otro método
      
      notifications("Proceso completado");
      
      // Usar métodos anónimos
      MathOperation subtract = delegate(int x, int y) { return x - y; };
      Console.WriteLine($"Resta (método anónimo): {subtract(10, 4)}");
      
      // Usar expresiones lambda
      MathOperation divide = (x, y) => x / y;
      Console.WriteLine($"División (lambda): {divide(20, 4)}");
      
      Console.WriteLine();
    }
    
    // =====================================
    // FUNC<T> - DELEGADOS QUE DEVUELVEN VALOR
    // =====================================
    static void FuncExamples()
    {
      Console.WriteLine("--- EJEMPLOS DE FUNC<T> ---");
      
      // Func<T> sin parámetros que devuelve int
      Func<int> getRandomNumber = () => new Random().Next(1, 100);
      Console.WriteLine($"Número aleatorio: {getRandomNumber()}");
      
      // Func<T, TResult> con un parámetro
      Func<int, int> square = x => x * x;
      Console.WriteLine($"Cuadrado de 5: {square(5)}");
      
      // Func<T1, T2, TResult> con múltiples parámetros
      Func<int, int, int> power = (baseNum, exponent) => 
      {
        int result = 1;
        for (int i = 0; i < exponent; i++)
          result *= baseNum;
        return result;
      };
      Console.WriteLine($"2 elevado a la 3: {power(2, 3)}");
      
      // Func con tipos complejos
      Func<string, int, string> formatMessage = (text, count) => 
        $"Mensaje: {text} (repetido {count} veces)";
      Console.WriteLine(formatMessage("Hola", 3));
      
      // Usar Func en colecciones
      List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
      Func<int, bool> isEven = n => n % 2 == 0;
      var evenNumbers = numbers.Where(isEven).ToList();
      Console.WriteLine($"Números pares: [{string.Join(", ", evenNumbers)}]");
      
      Console.WriteLine();
    }
    
    // =====================================
    // ACTION<T> - DELEGADOS QUE NO DEVUELVEN VALOR
    // =====================================
    static void ActionExamples()
    {
      Console.WriteLine("--- EJEMPLOS DE ACTION<T> ---");
      
      // Action sin parámetros
      Action greet = () => Console.WriteLine("¡Hola mundo!");
      greet();
      
      // Action<T> con un parámetro
      Action<string> printMessage = message => Console.WriteLine($"Mensaje: {message}");
      printMessage("Este es un Action<T>");
      
      // Action<T1, T2> con múltiples parámetros
      Action<string, int> repeatMessage = (text, times) =>
      {
        for (int i = 0; i < times; i++)
          Console.WriteLine($"{i + 1}: {text}");
      };
      repeatMessage("Repetir esto", 3);
      
      // Action con operaciones complejas
      Action<List<int>> processNumbers = numbers =>
      {
        Console.WriteLine($"Procesando {numbers.Count} números:");
        Console.WriteLine($"Suma: {numbers.Sum()}");
        Console.WriteLine($"Promedio: {numbers.Average():F2}");
        Console.WriteLine($"Máximo: {numbers.Max()}");
      };
      
      List<int> data = new List<int> { 10, 20, 30, 40, 50 };
      processNumbers(data);
      
      Console.WriteLine();
    }
    
    // =====================================
    // PREDICATE<T> - DELEGADOS PARA CONDICIONES
    // =====================================
    static void PredicateExamples()
    {
      Console.WriteLine("--- EJEMPLOS DE PREDICATE<T> ---");
      
      // Predicate básico
      Predicate<int> isPositive = x => x > 0;
      Console.WriteLine($"¿5 es positivo? {isPositive(5)}");
      Console.WriteLine($"¿-3 es positivo? {isPositive(-3)}");
      
      // Predicate con objetos
      Predicate<string> isValidEmail = email => 
        !string.IsNullOrEmpty(email) && email.Contains("@") && email.Contains(".");
      
      Console.WriteLine($"¿'user@example.com' es email válido? {isValidEmail("user@example.com")}");
      Console.WriteLine($"¿'invalid-email' es email válido? {isValidEmail("invalid-email")}");
      
      // Usar Predicate con listas
      List<int> numbers = new List<int> { -5, -2, 0, 3, 7, 12, -8 };
      
      Predicate<int> isEven = n => n % 2 == 0;
      Predicate<int> isNegative = n => n < 0;
      Predicate<int> isLarge = n => n > 10;
      
      // Encontrar elementos que cumplan condiciones
      var evenNumbers = numbers.FindAll(isEven);
      var negativeNumbers = numbers.FindAll(isNegative);
      var largeNumbers = numbers.FindAll(isLarge);
      
      Console.WriteLine($"Números originales: [{string.Join(", ", numbers)}]");
      Console.WriteLine($"Números pares: [{string.Join(", ", evenNumbers)}]");
      Console.WriteLine($"Números negativos: [{string.Join(", ", negativeNumbers)}]");
      Console.WriteLine($"Números grandes (>10): [{string.Join(", ", largeNumbers)}]");
      
      // Combinar predicados
      Predicate<int> isEvenAndPositive = n => isEven(n) && isPositive(n);
      var evenPositiveNumbers = numbers.FindAll(isEvenAndPositive);
      Console.WriteLine($"Números pares y positivos: [{string.Join(", ", evenPositiveNumbers)}]");
      
      Console.WriteLine();
    }
    
    // =====================================
    // FUNCIONES PURAS
    // =====================================
    static void PureFunctionExamples()
    {
      Console.WriteLine("--- EJEMPLOS DE FUNCIONES PURAS ---");
      
      // Función pura: siempre devuelve el mismo resultado para las mismas entradas
      // No tiene efectos secundarios
      Func<int, int, int> pureAdd = (a, b) => a + b;
      
      // Función pura para calcular el área de un círculo
      Func<double, double> calculateCircleArea = radius => Math.PI * radius * radius;
      
      // Función pura para transformar cadenas
      Func<string, string> toUpperAndTrim = text => text?.Trim().ToUpper() ?? "";
      
      // Función pura para operaciones matemáticas complejas
      Func<List<int>, double> calculateVariance = numbers =>
      {
        if (numbers == null || numbers.Count == 0) return 0;
        
        double mean = numbers.Average();
        double sumOfSquares = numbers.Sum(x => Math.Pow(x - mean, 2));
        return sumOfSquares / numbers.Count;
      };
      
      // Ejemplos de uso
      Console.WriteLine($"Suma pura: {pureAdd(5, 3)}");
      Console.WriteLine($"Suma pura (mismo resultado): {pureAdd(5, 3)}");
      
      Console.WriteLine($"Área del círculo (radio 5): {calculateCircleArea(5):F2}");
      Console.WriteLine($"Transformar texto: '{toUpperAndTrim("  hola mundo  ")}' ");
      
      List<int> sampleData = new List<int> { 2, 4, 6, 8, 10 };
      Console.WriteLine($"Varianza de {string.Join(", ", sampleData)}: {calculateVariance(sampleData):F2}");
      
      // Demostrar inmutabilidad - las funciones puras no modifican los datos originales
      var originalText = "  ejemplo  ";
      var transformedText = toUpperAndTrim(originalText);
      Console.WriteLine($"Texto original: '{originalText}'");
      Console.WriteLine($"Texto transformado: '{transformedText}'");
      Console.WriteLine($"El original no cambió: '{originalText}'");
      
      Console.WriteLine();
    }
    
    // =====================================
    // FUNCIONES DE ORDEN SUPERIOR
    // =====================================
    static void HigherOrderFunctionExamples()
    {
      Console.WriteLine("--- EJEMPLOS DE FUNCIONES DE ORDEN SUPERIOR ---");
      
      // Función que toma otra función como parámetro
      Func<List<int>, Func<int, bool>, List<int>> filterNumbers = (numbers, condition) =>
        numbers.Where(condition).ToList();
      
      // Función que devuelve otra función
      Func<int, Func<int, int>> createMultiplier = factor => x => x * factor;
      
      // Función que toma y devuelve funciones
      Func<Func<int, int>, Func<int, int>, Func<int, int>> combineOperations = 
        (op1, op2) => x => op2(op1(x));
      
      List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
      
      // Usar función de orden superior con diferentes condiciones
      var evenNumbers = filterNumbers(numbers, x => x % 2 == 0);
      var largeNumbers = filterNumbers(numbers, x => x > 5);
      var primeNumbers = filterNumbers(numbers, IsPrime);
      
      Console.WriteLine($"Números originales: [{string.Join(", ", numbers)}]");
      Console.WriteLine($"Números pares: [{string.Join(", ", evenNumbers)}]");
      Console.WriteLine($"Números > 5: [{string.Join(", ", largeNumbers)}]");
      Console.WriteLine($"Números primos: [{string.Join(", ", primeNumbers)}]");
      
      // Crear funciones especializadas usando funciones de orden superior
      var doubler = createMultiplier(2);
      var tripler = createMultiplier(3);
      
      Console.WriteLine($"Doblar 5: {doubler(5)}");
      Console.WriteLine($"Triplicar 4: {tripler(4)}");
      
      // Combinar operaciones
      Func<int, int> addTen = x => x + 10;
      Func<int, int> square = x => x * x;
      
      var addThenSquare = combineOperations(addTen, square);
      var squareThenAdd = combineOperations(square, addTen);
      
      Console.WriteLine($"(5 + 10)² = {addThenSquare(5)}");
      Console.WriteLine($"5² + 10 = {squareThenAdd(5)}");
      
      // Ejemplo avanzado: función que aplica múltiples transformaciones
      Func<List<int>, List<Func<int, int>>, List<int>> applyTransformations = 
        (data, transformations) =>
        {
          var result = new List<int>();
          foreach (var number in data)
          {
            int transformed = number;
            foreach (var transform in transformations)
            {
              transformed = transform(transformed);
            }
            result.Add(transformed);
          }
          return result;
        };
      
      var transformations = new List<Func<int, int>>
      {
        x => x * 2,      // Doblar
        x => x + 1,      // Sumar 1
        x => x * x       // Elevar al cuadrado
      };
      
      var smallNumbers = new List<int> { 1, 2, 3 };
      var transformed = applyTransformations(smallNumbers, transformations);
      
      Console.WriteLine($"Aplicar transformaciones a {string.Join(", ", smallNumbers)}:");
      Console.WriteLine($"Resultado: [{string.Join(", ", transformed)}]");
      Console.WriteLine("Transformaciones: doblar -> sumar 1 -> elevar al cuadrado");
      
      Console.WriteLine();
    }
    
    // Función auxiliar para verificar números primos
    static bool IsPrime(int number)
    {
      if (number < 2) return false;
      if (number == 2) return true;
      if (number % 2 == 0) return false;
      
      for (int i = 3; i <= Math.Sqrt(number); i += 2)
      {
        if (number % i == 0) return false;
      }
      return true;
    }
  }
}