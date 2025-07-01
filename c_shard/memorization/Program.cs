using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace MemoizationExamples
{
  // Ejemplo 1: Fibonacci con Memoization
  public class FibonacciMemoization
  {
    private static Dictionary<int, long> fibonacciCache = new Dictionary<int, long>();

    public static long CalculateFibonacci(int n)
    {
      // Verificar si el resultado ya está en cache
      if (fibonacciCache.ContainsKey(n))
      {
        Console.WriteLine($"Obteniendo Fibonacci({n}) desde cache: {fibonacciCache[n]}");
        return fibonacciCache[n];
      }

      long result;
      
      // Casos base
      if (n <= 1)
      {
        result = n;
      }
      else
      {
        // Calcular recursivamente y almacenar en cache
        result = CalculateFibonacci(n - 1) + CalculateFibonacci(n - 2);
      }

      // Guardar el resultado en cache
      fibonacciCache[n] = result;
      Console.WriteLine($"Calculando y guardando Fibonacci({n}): {result}");
      
      return result;
    }

    public static void ClearCache()
    {
      fibonacciCache.Clear();
    }
  }

  // Ejemplo 2: Factorial con Memoization
  public class FactorialMemoization
  {
    private static Dictionary<int, long> factorialCache = new Dictionary<int, long>();

    public static long CalculateFactorial(int n)
    {
      // Validar entrada
      if (n < 0)
      {
        throw new ArgumentException("El factorial no está definido para números negativos");
      }

      // Verificar si el resultado ya está en cache
      if (factorialCache.ContainsKey(n))
      {
        Console.WriteLine($"Obteniendo Factorial({n}) desde cache: {factorialCache[n]}");
        return factorialCache[n];
      }

      long result;

      // Caso base
      if (n == 0 || n == 1)
      {
        result = 1;
      }
      else
      {
        // Calcular recursivamente
        result = n * CalculateFactorial(n - 1);
      }

      // Guardar el resultado en cache
      factorialCache[n] = result;
      Console.WriteLine($"Calculando y guardando Factorial({n}): {result}");

      return result;
    }

    public static void ClearCache()
    {
      factorialCache.Clear();
    }
  }



  /*
    Prueba de las funciones: Fibonacci y Factorial usando el Patrón Memoization
    Para esto se usa una clase y una variable para almacenar los resultados previos
  */
  class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine("=== EJEMPLO 1: FIBONACCI CON MEMOIZATION ===");
      Console.WriteLine();

      // Primer cálculo - se calculan todos los valores
      Console.WriteLine("Primera llamada a Fibonacci(10):");
      var stopwatch = Stopwatch.StartNew();
      long fib10 = FibonacciMemoization.CalculateFibonacci(10);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fib10}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");
      Console.WriteLine();

      // Segunda llamada - usa valores en cache
      Console.WriteLine("Segunda llamada a Fibonacci(10):");
      stopwatch.Restart();
      fib10 = FibonacciMemoization.CalculateFibonacci(10);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fib10}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");
      Console.WriteLine();

      // Calcular un número mayor - reutiliza cache parcialmente
      Console.WriteLine("Calculando Fibonacci(12) (reutiliza cache previo):");
      long fib12 = FibonacciMemoization.CalculateFibonacci(12);
      Console.WriteLine($"Resultado: {fib12}");
      Console.WriteLine();

      Console.WriteLine("=== EJEMPLO 2: FACTORIAL CON MEMOIZATION ===");
      Console.WriteLine();

      // Limpiar cache del ejemplo anterior
      FibonacciMemoization.ClearCache();

      // Primer cálculo de factorial
      Console.WriteLine("Primera llamada a Factorial(8):");
      stopwatch.Restart();
      long fact8 = FactorialMemoization.CalculateFactorial(8);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fact8}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");
      Console.WriteLine();

      // Segunda llamada - usa cache
      Console.WriteLine("Segunda llamada a Factorial(8):");
      stopwatch.Restart();
      fact8 = FactorialMemoization.CalculateFactorial(8);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fact8}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");
      Console.WriteLine();

      // Calcular factorial mayor - reutiliza cache
      Console.WriteLine("Calculando Factorial(10) (reutiliza cache previo):");
      long fact10 = FactorialMemoization.CalculateFactorial(10);
      Console.WriteLine($"Resultado: {fact10}");
      Console.WriteLine();

      Console.WriteLine("=== COMPARACION SIN MEMOIZATION ===");
      Console.WriteLine();

      // Ejemplo de Fibonacci sin memoization para comparar
      Console.WriteLine("Fibonacci(35) sin memoization:");
      stopwatch.Restart();
      long fibWithoutMemo = FibonacciWithoutMemoization(35);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fibWithoutMemo}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");
      Console.WriteLine();

      // Limpiar cache y calcular con memoization
      FibonacciMemoization.ClearCache();
      Console.WriteLine("Fibonacci(35) con memoization:");
      stopwatch.Restart();
      long fibWithMemo = FibonacciMemoization.CalculateFibonacci(35);
      stopwatch.Stop();
      Console.WriteLine($"Resultado: {fibWithMemo}");
      Console.WriteLine($"Tiempo: {stopwatch.ElapsedMilliseconds} ms");

      Console.WriteLine();
      Console.WriteLine("Presiona cualquier tecla para salir...");
      Console.ReadKey();
    }

    // Función auxiliar para demostrar Fibonacci sin memoization
    static long FibonacciWithoutMemoization(int n)
    {
      if (n <= 1)
        return n;
      return FibonacciWithoutMemoization(n - 1) + FibonacciWithoutMemoization(n - 2);
    }
  }
}