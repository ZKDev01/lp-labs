using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace ConcurrencyPrimitives {
  /*
    Implementación de Barrier usando Semáforos
    - Esta clase permite que un grupo de hilos se sincronicen en un punto específico.
    - Los hilos pueden llamar a `SignalAndWait` para indicar que han llegado al punto de sincronización.
    - Una vez que todos los hilos han llamado a `SignalAndWait`, se libera
  */
  public class CustomBarrier {
    private readonly int participantCount;
    private int currentCount;
    private readonly SemaphoreSlim barrierSemaphore;
    private readonly SemaphoreSlim mutexSemaphore;
    private int barrierGeneration;

    public CustomBarrier(int participantCount) {
      this.participantCount = participantCount;
      this.currentCount = 0;
      // semáforo para bloquear hilos hasta que todos lleguen 
      this.barrierSemaphore = new SemaphoreSlim(0, participantCount);
      // semáforo para proteger acceso concurrente a variables compartidas
      this.mutexSemaphore = new SemaphoreSlim(1, 1);
      this.barrierGeneration = 0;
    }

    public async Task SignalAndWait() {
      await mutexSemaphore.WaitAsync();
      currentCount++;

      // si todos los participantes han llegado
      if (currentCount == participantCount) {
        
        // despertar a todos los hilos que esperan en la barrera
        barrierSemaphore.Release(participantCount);
        
        // reiniciar el contador
        currentCount = 0; 

        // incrementar la generación
        barrierGeneration++; 

        // liberar el semáforo de mutex para permitir que otros hilos accedan
        mutexSemaphore.Release(); 

      } else {
        mutexSemaphore.Release();
        // esperar hasta que todos lleguen
        await barrierSemaphore.WaitAsync();
      }
    }
  }

  /*
    Implementación de Countdown usando Semáforos
    - Esta clase permite a los hilos esperar hasta que un contador llegue a cero.
    - Los hilos pueden decrementar el contador y esperar hasta que todos hayan
      decrecido el contador a cero.
  */
  public class CustomCountdownLatch
  {
    private int count;
    private readonly SemaphoreSlim waitSemaphore;
    private readonly SemaphoreSlim mutexSemaphore;

    public CustomCountdownLatch(int initialCount)
    {
      if (initialCount < 0)
      {
        throw new ArgumentOutOfRangeException(nameof(initialCount), "El valor inicial debe ser no negativo.");
      }
      this.count = initialCount;

      // semáforo inicializado en 0 para bloquear hilos que esperan
      this.waitSemaphore = new SemaphoreSlim(0, 1);

      // semáforo para proteger el contador
      this.mutexSemaphore = new SemaphoreSlim(1, 1);
    }

    public async Task CountDown()
    {
      await mutexSemaphore.WaitAsync();

      if (count <= 0)
      {
        mutexSemaphore.Release();
        throw new InvalidOperationException("El contador ya ha llegado a cero.");
      }
      
      count--; // decrementar el contador

      // si el contador llega a cero, liberar todos los hilos 
      if (count == 0)
      {
        waitSemaphore.Release();
      }

      mutexSemaphore.Release();
    }

    public async Task Wait()
    {
      await mutexSemaphore.WaitAsync();

      // si el contador ya es 0, no es necesario esperar
      if (count == 0)
      {
        mutexSemaphore.Release();
        return;
      }

      mutexSemaphore.Release();

      // esperar hasta que el contador llegue a 0
      await waitSemaphore.WaitAsync();

      // releaser para permitir que otros hilos también pasen
      waitSemaphore.Release();
    }

    public int CurrentCount 
    { 
      get 
      { 
        mutexSemaphore.Wait();
        var result = count;
        mutexSemaphore.Release();
        return result;
      } 
    }
  }

  /*
    Implementación de Monitor usando Semáforos
    - Esta clase permite a los hilos esperar y notificar de manera similar a un monitor 
      tradicional.
    - Los hilos pueden entrar en la sección crítica, esperar a que se les notifique,
      y notificar a otros hilos cuando han terminado su trabajo.
  */
  public class CustomMonitor
  {
    private readonly SemaphoreSlim mutexSemaphore;
    private readonly Queue<SemaphoreSlim> waitingQueue;
    private readonly SemaphoreSlim queueMutex;

    public CustomMonitor()
    {
      // semáforo para exclusión mutua del recurso protegido
      this.mutexSemaphore = new SemaphoreSlim(1, 1);

      // cola de semáforos para hilos esperando
      this.waitingQueue = new Queue<SemaphoreSlim>();

      // semáforo para proteger la cola de espera  
      this.queueMutex = new SemaphoreSlim(1, 1);
    }

    public async Task EnterAsync()
    {
      await mutexSemaphore.WaitAsync();
    }

    public void Exit()
    {
      mutexSemaphore.Release();
    }

    public async Task WaitAsync()
    {
      // crear semáforo personal para este hilo
      var personalSemaphore = new SemaphoreSlim(0, 1);

      await queueMutex.WaitAsync();
      waitingQueue.Enqueue(personalSemaphore);
      queueMutex.Release();

      // liberar el lock del monitor antes de esperar
      Exit();

      // esperar hasta ser notificado 
      await personalSemaphore.WaitAsync();

      // recuperar el lock del monitor
      await EnterAsync();
    }

    public async Task Pulse()
    {
      await queueMutex.WaitAsync();

      // despertar al primer hilo en la cola
      if (waitingQueue.Count > 0)
      {
        var semaphoreToSignal = waitingQueue.Dequeue();
        semaphoreToSignal.Release();
      }

      queueMutex.Release();
    }

    public async Task PulseAll()
    {
      await queueMutex.WaitAsync();

      // despertar todos los hilos en la cola
      while (waitingQueue.Count > 0)
      {
        var semaphoreToSignal = waitingQueue.Dequeue();
        semaphoreToSignal.Release();
      }

      queueMutex.Release();
    }
  }

  class Program
  {
    static async Task Main(string[] args)
    {
      Console.WriteLine("=== Ejemplo Básico de SemaphoreSlim ===");
      await BasicSemaphoreExample();
      Console.WriteLine();

      Console.WriteLine("=== Demostración de Custom Barrier ===");
      await DemostrateBarrier();
      Console.WriteLine();

      Console.WriteLine("=== Demostración de Custom Countdown Latch ===");
      await DemostrateCountdown();
      Console.WriteLine();

      Console.WriteLine("=== Demostración de Custom Monitor ===");
      await DemostrateMonitor();
      Console.WriteLine();
    }

    // Ejemplo básico de uso de SemaphoreSlim
    static async Task BasicSemaphoreExample()
    {
      var N = 3; // Número máximo de hilos concurrentes
      var T = 5; // Número total de hilos a iniciar
      var semaphore = new SemaphoreSlim(N); // Permite hasta 2 hilos concurrentes
      var tasks = new List<Task>();

      Console.WriteLine($"Iniciando {T} hilos con semáforo que permite solo {N} concurrentes...");

      for (int i = 0; i < T; i++)
      {
        int threadId = i;
        tasks.Add(Task.Run(async () =>
        {
          Console.WriteLine($"Hilo {threadId} esperando el semáforo...");
          await semaphore.WaitAsync(); // Espera asíncrona para adquirir el semáforo
          Console.WriteLine($"Hilo {threadId} ha adquirido el semáforo.");
          await Task.Delay(2000); // Simula trabajo
          Console.WriteLine($"Hilo {threadId} libera el semáforo.");
          semaphore.Release();
        }));
      }

      await Task.WhenAll(tasks);
      Console.WriteLine("Todos los hilos han terminado.");
    }

    static async Task DemostrateBarrier()
    {
      const int participantCount = 4;
      var barrier = new CustomBarrier(participantCount);
      var tasks = new List<Task>();

      Console.WriteLine($"Iniciando {participantCount} participantes para demostrar barrera...");

      for (int i = 0; i < participantCount; i++)
      {
        int participantId = i;
        tasks.Add(Task.Run(async () =>
        {
          // Fase 1: Trabajo inicial
          var workTime = Random.Shared.Next(1000, 3000);
          Console.WriteLine($"Participante {participantId} trabajando por {workTime}ms...");
          await Task.Delay(workTime);
          
          Console.WriteLine($"Participante {participantId} llegó a la BARRERA - Esperando a otros...");
          await barrier.SignalAndWait();
          Console.WriteLine($"Participante {participantId} cruzó la BARRERA");
        }));
      }
      
      await Task.WhenAll(tasks);
      Console.WriteLine("Todos los participantes han cruzado la BARRERA");
    }

    static async Task DemostrateCountdown() 
    {
      const int initialCount = 3;
      var countdown = new CustomCountdownLatch(initialCount);
      var tasks = new List<Task>();

      Console.WriteLine($"Iniciando countdown con contador inicial: {initialCount}");

      // Hilos que esperan el countdown
      for (int i = 0; i < 2; i++)
      {
        int waiterId = i;
        tasks.Add(Task.Run(async () =>
        {
          Console.WriteLine($"Hilo esperador {waiterId} esperando countdown...");
          await countdown.Wait();
          Console.WriteLine($"Hilo esperador {waiterId} -> Countdown completado (Continuando)");
        }));
      }

      // Hilos que hacen countdown
      for (int i = 0; i < initialCount; i++)
      {
        int counterId = i;
        tasks.Add(Task.Run(async () =>
        {
          await Task.Delay(Random.Shared.Next(1000, 2000)); // Simular trabajo
          Console.WriteLine($"Contador {counterId} haciendo countdown... (Restante: {countdown.CurrentCount - 1})");
          await countdown.CountDown();
          Console.WriteLine($"Contador {counterId} completó countdown");
        }));
      }

      await Task.WhenAll(tasks);
      Console.WriteLine("Demostración de countdown completada");
    }

    static async Task DemostrateMonitor() 
    {
      var monitor = new CustomMonitor();
      int sharedCounter = 0;
      var tasks = new List<Task>();

      Console.WriteLine("Demostrando uso de Custom Monitor con contador compartido...");

      // Hilos que incrementan el contador
      for (int i = 0; i < 3; i++)
      {
        int threadId = i;
        tasks.Add(Task.Run(async () =>
        {
          for (int j = 0; j < 2; j++)
          {
            await monitor.EnterAsync();
            
            int oldValue = sharedCounter;
            await Task.Delay(100); // Simular trabajo crítico
            sharedCounter++;
            
            Console.WriteLine($"Hilo {threadId} incrementó contador: {oldValue} -> {sharedCounter}");
            
            // Notificar si llegamos a cierto valor
            if (sharedCounter >= 3)
            {
              Console.WriteLine($"Hilo {threadId} notificando: contador llegó a {sharedCounter}");
              await monitor.PulseAll();
            }
            
            monitor.Exit();
            await Task.Delay(200); // Pausa entre incrementos
          }
        }));
      }

      await Task.WhenAll(tasks);
      Console.WriteLine($"Demostración de monitor completada. Contador final: {sharedCounter}");
    }
  }
}