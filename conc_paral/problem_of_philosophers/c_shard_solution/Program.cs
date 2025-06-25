using System;
using System.Threading;
using System.Threading.Tasks;

public class DiningPhilosophers
{
    private readonly int numPhilosophers;
    private readonly Semaphore[] forks;
    private readonly Random random = new Random();
    private volatile bool isRunning = true;

    public DiningPhilosophers(int numberOfPhilosophers = 5)
    {
        numPhilosophers = numberOfPhilosophers;
        forks = new Semaphore[numPhilosophers];
        
        // Inicializar semáforos para los tenedores
        for (int i = 0; i < numPhilosophers; i++)
        {
            forks[i] = new Semaphore(1, 1);
        }
    }

    public async Task StartDining(int durationSeconds = 30)
    {
        Console.WriteLine($"=== Iniciando simulación con {numPhilosophers} filósofos ===");
        Console.WriteLine("Presiona cualquier tecla para detener la simulación...\n");

        // Crear tareas para cada filósofo
        var tasks = new Task[numPhilosophers];
        for (int i = 0; i < numPhilosophers; i++)
        {
            int philosopherId = i;
            tasks[i] = Task.Run(() => PhilosopherLifeCycle(philosopherId));
        }

        // Detener después del tiempo especificado o al presionar una tecla
        var keyTask = Task.Run(() => Console.ReadKey());
        var timeoutTask = Task.Delay(TimeSpan.FromSeconds(durationSeconds));
        
        await Task.WhenAny(keyTask, timeoutTask);
        
        isRunning = false;
        Console.WriteLine("\n\n=== Deteniendo simulación ===");
        
        // Esperar a que todos los filósofos terminen
        await Task.WhenAll(tasks);
        Console.WriteLine("Simulación terminada.");
    }

    private void PhilosopherLifeCycle(int id)
    {
        while (isRunning)
        {
            Think(id);
            if (isRunning) TryToEat(id);
        }
    }

    private void Think(int id)
    {
        Console.WriteLine($"Filósofo {id} está pensando... 🤔");
        Thread.Sleep(random.Next(1000, 3000)); // Pensar entre 1-3 segundos
    }

    private void TryToEat(int id)
    {
        int leftFork = id;
        int rightFork = (id + 1) % numPhilosophers;
        
        // Prevenir deadlock: el último filósofo toma los tenedores en orden inverso
        if (id == numPhilosophers - 1)
        {
            (leftFork, rightFork) = (rightFork, leftFork);
        }

        Console.WriteLine($"Filósofo {id} quiere comer - buscando tenedores {leftFork} y {rightFork}");

        // Intentar tomar el primer tenedor
        forks[leftFork].WaitOne();
        Console.WriteLine($"Filósofo {id} tomó el tenedor {leftFork}");

        // Intentar tomar el segundo tenedor
        forks[rightFork].WaitOne();
        Console.WriteLine($"Filósofo {id} tomó el tenedor {rightFork}");

        // Comer
        Eat(id);

        // Liberar tenedores
        forks[rightFork].Release();
        Console.WriteLine($"Filósofo {id} liberó el tenedor {rightFork}");
        
        forks[leftFork].Release();
        Console.WriteLine($"Filósofo {id} liberó el tenedor {leftFork}");
    }

    private void Eat(int id)
    {
        Console.WriteLine($"🍝 Filósofo {id} está COMIENDO 🍝");
        Thread.Sleep(random.Next(1000, 2000)); // Comer entre 1-2 segundos
        Console.WriteLine($"Filósofo {id} terminó de comer");
    }

    public void Dispose()
    {
        foreach (var fork in forks)
        {
            fork?.Dispose();
        }
    }
}

// Versión alternativa usando Monitor para prevención de deadlock
public class DiningPhilosophersWithMonitor
{
    private readonly int numPhilosophers;
    private readonly object[] forks;
    private readonly Random random = new Random();
    private volatile bool isRunning = true;

    public DiningPhilosophersWithMonitor(int numberOfPhilosophers = 5)
    {
        numPhilosophers = numberOfPhilosophers;
        forks = new object[numPhilosophers];
        
        for (int i = 0; i < numPhilosophers; i++)
        {
            forks[i] = new object();
        }
    }

    public async Task StartDining(int durationSeconds = 30)
    {
        Console.WriteLine($"=== Iniciando simulación con Monitor - {numPhilosophers} filósofos ===");
        Console.WriteLine("Presiona cualquier tecla para detener...\n");

        var tasks = new Task[numPhilosophers];
        for (int i = 0; i < numPhilosophers; i++)
        {
            int philosopherId = i;
            tasks[i] = Task.Run(() => PhilosopherLifeCycle(philosopherId));
        }

        var keyTask = Task.Run(() => Console.ReadKey());
        var timeoutTask = Task.Delay(TimeSpan.FromSeconds(durationSeconds));
        
        await Task.WhenAny(keyTask, timeoutTask);
        
        isRunning = false;
        Console.WriteLine("\n\n=== Deteniendo simulación ===");
        
        await Task.WhenAll(tasks);
        Console.WriteLine("Simulación terminada.");
    }

    private void PhilosopherLifeCycle(int id)
    {
        while (isRunning)
        {
            Think(id);
            if (isRunning) TryToEatWithTimeout(id);
        }
    }

    private void Think(int id)
    {
        Console.WriteLine($"Filósofo {id} está pensando... 🤔");
        Thread.Sleep(random.Next(1000, 3000));
    }

    private void TryToEatWithTimeout(int id)
    {
        int leftFork = id;
        int rightFork = (id + 1) % numPhilosophers;
        
        Console.WriteLine($"Filósofo {id} intenta comer - necesita tenedores {leftFork} y {rightFork}");

        // Usar timeout para evitar deadlock
        bool gotFirstFork = false;
        bool gotSecondFork = false;

        try
        {
            if (Monitor.TryEnter(forks[leftFork], TimeSpan.FromMilliseconds(1000)))
            {
                gotFirstFork = true;
                Console.WriteLine($"Filósofo {id} tomó el tenedor {leftFork}");

                if (Monitor.TryEnter(forks[rightFork], TimeSpan.FromMilliseconds(1000)))
                {
                    gotSecondFork = true;
                    Console.WriteLine($"Filósofo {id} tomó el tenedor {rightFork}");
                    
                    // Comer
                    Eat(id);
                }
                else
                {
                    Console.WriteLine($"Filósofo {id} no pudo tomar el tenedor {rightFork} - esperará");
                }
            }
            else
            {
                Console.WriteLine($"Filósofo {id} no pudo tomar el tenedor {leftFork} - esperará");
            }
        }
        finally
        {
            if (gotSecondFork)
            {
                Monitor.Exit(forks[rightFork]);
                Console.WriteLine($"Filósofo {id} liberó el tenedor {rightFork}");
            }
            
            if (gotFirstFork)
            {
                Monitor.Exit(forks[leftFork]);
                Console.WriteLine($"Filósofo {id} liberó el tenedor {leftFork}");
            }
        }
    }

    private void Eat(int id)
    {
        Console.WriteLine($"🍝 Filósofo {id} está COMIENDO 🍝");
        Thread.Sleep(random.Next(1000, 2000));
        Console.WriteLine($"Filósofo {id} terminó de comer");
    }
}

// Programa principal
class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("Selecciona la implementación:");
        Console.WriteLine("1. Con Semáforos (prevención de deadlock por orden)");
        Console.WriteLine("2. Con Monitor y Timeout");
        Console.Write("Opción (1 o 2): ");
        
        var option = Console.ReadLine();
        
        Console.Write("Número de filósofos (default 5): ");
        var numInput = Console.ReadLine();
        int numPhilosophers = string.IsNullOrEmpty(numInput) ? 5 : int.Parse(numInput);
        
        Console.Write("Duración en segundos (default 30): ");
        var durationInput = Console.ReadLine();
        int duration = string.IsNullOrEmpty(durationInput) ? 30 : int.Parse(durationInput);

        try
        {
            if (option == "2")
            {
                var simulation = new DiningPhilosophersWithMonitor(numPhilosophers);
                await simulation.StartDining(duration);
            }
            else
            {
                var simulation = new DiningPhilosophers(numPhilosophers);
                await simulation.StartDining(duration);
                simulation.Dispose();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        
        Console.WriteLine("\nPresiona cualquier tecla para salir...");
        Console.ReadKey();
    }
}