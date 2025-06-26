using System;
using System.Threading;
using System.Threading.Tasks;

class Program
{
  static async Task Main(string[] args)
  {
    Console.WriteLine("Ejemplos de Tasks en C#");

    Console.WriteLine("Ejemplo 1: Task básico");
    Task basicTask = Task.Run(() =>
    {
      Console.WriteLine($"Ejecutando tarea básica en hilo: {Thread.CurrentThread.ManagedThreadId}");
      Thread.Sleep(1000); // Simula trabajo
      Console.WriteLine("Tarea básica completada.");
    });

    await basicTask;
    Console.WriteLine("Tarea básica finalizada.\n");
    Thread.Sleep(1000); // Espera para ver el resultado

    Console.WriteLine("Ejemplo 2: Task con retorno de valor");
    Task<int> taskWithReturn = Task.Run(() =>
    {
      Console.WriteLine($"Ejecutando tarea con retorno en hilo: {Thread.CurrentThread.ManagedThreadId}");
      Thread.Sleep(1000); // Simula trabajo
      return 42; // Retorna un valor
    });
    int result = await taskWithReturn;
    Console.WriteLine($"Tarea con retorno completada. Resultado: {result}\n");
    Thread.Sleep(1000); // Espera para ver el resultado

    Console.WriteLine("Ejemplo 3: Múltiples Task ejecutándose en paralelo");
    Task task1 = Task.Run(() => SimulateWork("A", 2000));
    Task task2 = Task.Run(() => SimulateWork("B", 1500));
    Task task3 = Task.Run(() => SimulateWork("C", 1000));

    // Espera a que todas las tareas finalicen
    await Task.WhenAll(task1, task2, task3);
    Console.WriteLine("Todas las tareas paralelas completadas.\n");

    Console.WriteLine("Ejemplo 4: Task con cancelación");
    await SimulateWorkWithCancellation();
    Console.WriteLine("");

    Console.WriteLine("Ejemplo 5: Manejo de excepciones en Task");
    await SimulateWorkWithException();
    Console.WriteLine("");

    Console.WriteLine("Ejemplo 6: Task continuations");
    await SimulateTaskContinuation();
    Console.WriteLine("");

    Console.WriteLine("Ejemplo 7: Task continuations con retorno de valor");
    await SimulateTasContinuationWithReturn();

  }

  static void SimulateWork(string taskName, int duration)
  {
    Console.WriteLine($"Tarea {taskName} iniciada en hilo: {Thread.CurrentThread.ManagedThreadId}");
    Thread.Sleep(duration); // Simula trabajo
    Console.WriteLine($"Tarea {taskName} completada.");
  }

  static async Task SimulateWorkWithCancellation()
  {
    using (CancellationTokenSource cts = new CancellationTokenSource())
    {
      // cancelar después de 2 segundos
      try
      {
        Task longRunningTask = Task.Run(async () =>
        {
          Console.WriteLine($"Tarea larga iniciada en hilo: {Thread.CurrentThread.ManagedThreadId}");
          for (int i = 0; i < 5; i++)
          {
            cts.Token.ThrowIfCancellationRequested();
            Console.WriteLine($"Trabajando en la tarea larga... Iteración {i + 1}/5");
            await Task.Delay(1000, cts.Token); // Simula trabajo
          }
          Console.WriteLine("Tarea larga completada.");
        }, cts.Token);

        await longRunningTask;
        Console.WriteLine("Tarea larga finalizada.");
      }
      catch (OperationCanceledException)
      {
        Console.WriteLine("Task fue cancelada.");
      }
    }
  }

  static async Task SimulateWorkWithException()
  {
    try
    {
      await Task.Run(() =>
      {
        Console.WriteLine($"Tarea con excepción iniciada en hilo: {Thread.CurrentThread.ManagedThreadId}");
        Thread.Sleep(1000); // Simula trabajo
        throw new InvalidOperationException("Error simulado en la tarea.");
      });
    }
    catch (InvalidOperationException ex)
    {
      Console.WriteLine($"Excepción capturada: {ex.Message}");
    }
  }

  static async Task SimulateTaskContinuation()
  {
      Task<string> initialTask = Task.Run(() =>
      {
        Console.WriteLine($"Tarea inicial en hilo: {Thread.CurrentThread.ManagedThreadId}");
        Thread.Sleep(1000); // Simula trabajo
        return "Resultado de la tarea inicial";
      });
  
      Task continuationTask = initialTask.ContinueWith(t =>
      {
        Console.WriteLine($"Continuación de la tarea en hilo: {Thread.CurrentThread.ManagedThreadId}");
        Console.WriteLine($"Resultado de la tarea inicial: {t.Result}");
      });
  
      await continuationTask;
      Console.WriteLine("Continuación de la tarea finalizada.");
  }

  static async Task SimulateTasContinuationWithReturn()
  {
    Task<int> initialTask = Task.Run(() =>
    {
      Console.WriteLine($"Tarea inicial con retorno en hilo: {Thread.CurrentThread.ManagedThreadId}");
      Thread.Sleep(1000); // Simula trabajo
      return 100; // Retorna un valor
    });

    Task continuationTask = initialTask.ContinueWith(t =>
    {
      Console.WriteLine($"Continuación de la tarea con retorno en hilo: {Thread.CurrentThread.ManagedThreadId}");
      Console.WriteLine($"Resultado de la tarea inicial: {t.Result}");
    });

    await continuationTask;
    Console.WriteLine("Continuación de la tarea con retorno finalizada.");
  }

}