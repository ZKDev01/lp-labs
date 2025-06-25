using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace ConcurrencyPrimitives {
  /*
    Implementación de Barrier usando Semáforos
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

  /*
    Implementación de Countdown usando Semáforos
  */
  public class CustomCountdownLatch {
    private int count;
    private readonly SemaphoreSlim waitSemaphore;
    private readonly SemaphoreSlim mutexSemaphore;
    
    public CustomCountdownLatch(int initialCount) {
      if (initialCount < 0) { 
      throw new ArgumentOutOfRangeException(nameof(initialCount), "El valor inicial debe ser no negativo."); 
      }
      this.count = initialCount;
      
      // semáforo inicializado en 0 para bloquear hilos que esperan
      this.waitSemaphore = new SemaphoreSlim(0, 1);
      
      // semáforo para proteger el contador
      this.mutexSemaphore = new SemaphoreSlim(1, 1);
    }
    
    public void CountDown() {
      if (count <= 0) {
        throw new InvalidOperationException("El contador ya ha llegado a cero.");
      }      
      count--; // decrementar el contador

      // si el contador llega a cero, liberar todos los hilos 
      if (count == 0) {
        waitSemaphore.Release();
      }

      mutexSemaphore.Release();
    }

    public async Task Wait() {
      await mutexSemaphore.WaitAsync();

      // si el contador ya es 0, no es necesario esperar
      if (count == 0) {
        mutexSemaphore.Release();
        return;
      }

      mutexSemaphore.Release();

      // esperar hasta que el contador llegue a 0
      await waitSemaphore.WaitAsync();

      // releaser para permitir que otros hilos también pasen
      waitSemaphore.Release();
    }
  }

  /*
    Implementación de Monitor usando Semáforos
  */
  public class CustomMonitor {
    private readonly SemaphoreSlim mutexSemaphore;
    private readonly Queue<SemaphoreSlim> waitingQueue;
    private readonly SemaphoreSlim queueMutex;

    public CustomMonitor() {
      // semáforo para exclusión mutua del recurso protegido
      this.mutexSemaphore = new SemaphoreSlim(1, 1);

      // cola de semáforos para hilos esperando
      this.waitingQueue = new Queue<SemaphoreSlim>(); 

      // semáforo para proteger la cola de espera  
      this.queueMutex = new SemaphoreSlim(1, 1);      
    }

    public async Task EnterAsync() {
      await mutexSemaphore.WaitAsync();
    }

    public void Exit() {
      mutexSemaphore.Release();
    }

    public async Task WaitAsync() {
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

    public async Task Pulse() {
      await queueMutex.WaitAsync();

      // despertar al primer hilo en la cola
      if (waitingQueue.Count > 0) {
        var semaphoreToSignal = waitingQueue.Dequeue();
        semaphoreToSignal.Release();
      }

      queueMutex.Release();
    }

    public async Task PulseAll() {
      await queueMutex.WaitAsync();

      // despertar todos los hilos en la cola
      while (waitingQueue.Count > 0) {
        var semaphoreToSignal = waitingQueue.Dequeue();
        semaphoreToSignal.Release();
      }

      queueMutex.Release();
    }
  }



  class Program {
    static async Task Main(string[] args) {
      


      // demostración del Barrier
      await DemostrateBarrier();

      // demostración del Countdown
      //await DemostrateCountdown();

      // demostración del Monitor
      //await DemostrateMonitor();
    }


    static async Task DemostrateBarrier() {
      const int participantCount = 3;
      var barrier = new CustomBarrier(participantCount);
      var tasks = new List<Task>();

      for (int i = 0; i < participantCount; i++) {
        int participantId = i; 
        tasks.Add(Task.Run(async () => {
          await Task.Delay(Random.Shared.Next(1000, 3000)); // simular trabajo
          Console.WriteLine($"Participante {participantId} ha llegado a la barrera");
          await barrier.SignalAndWait();
          Console.WriteLine($"Participante {participantId} ha cruzado la barrera");
        }));
      }
      await Task.WhenAll(tasks);
      Console.WriteLine("Todos los hilos completaron el barrier");
    }


/*


    static async Task DemostrateCountdown() {

    }

    static async Task DemostrateMonitor() {

    }


*/

  }

}}