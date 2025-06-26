using System;
using System.Threading;
using System.Threading.Tasks;

/*
La clase `DiningPhilosophers` simula N filósofos
- Se usan los semáforos para los tenedores: cada tenedor se 
  representa con un semáforo inicializado en 1, lo que 
  significa que solo un filósofo puede usarlo a la vez. 
- Para prevenir los deadlocks, el último filósofo toma los
  tenedores en orden inverso.
*/

public class DiningPhilosophers
{
    private readonly int numPhilosophers;
    private readonly Semaphore[] forks;
    private readonly Random random = new Random();
    private int[] counter;

    /// <summary>
    /// Constructor que inicializa el número de filósofos y los semáforos para los tenedores.
    /// Por defecto, se crean 5 filósofos.
    /// </summary>
    /// <param name="numberOfPhilosophers"></param>
    public DiningPhilosophers(int numberOfPhilosophers = 5)
    {
        numPhilosophers = numberOfPhilosophers;
        forks = new Semaphore[numPhilosophers];
        counter = new int[numPhilosophers];
        // Inicializar semáforos para los tenedores, cada uno con un valor inicial de 1 (disponible)
        for (int i = 0; i < numPhilosophers; i++)
        {
            // Cada tenedor es un semáforo binario (1 disponible) 
            forks[i] = new Semaphore(1, 1); 
            counter[i] = 0;
        }
    }


    /// <summary>
    /// Inicia la simulación de los filósofos comiendo.
    /// La simulación durará el tiempo especificado en segundos.
    /// </summary>
    /// <param name="target"></param>
    /// <returns></returns>
    public async Task StartDining(int target = 3)
    {
        Console.WriteLine($"Iniciando simulación con {numPhilosophers} filósofos, cada uno debe comer {target} veces");
        
        // Crear tareas para cada filósofo
        var tasks = new Task[numPhilosophers];
        for (int i = 0; i < numPhilosophers; i++)
        {
            int philosopherId = i;
            // Cada filósofo corre en su propia tarea, ejecutando su ciclo de vida de manera concurrente 
            tasks[i] = Task.Run(() => PhilosopherLifeCycle(philosopherId, target));
        }

        await Task.WhenAll(tasks);
        Console.WriteLine("Simulación terminada");
    }

    private void PhilosopherLifeCycle(int id, int target)
    {
        while (counter[id] < target)
        {
            Think(id);
            TryToEat(id);
        }
    }

    private void Think(int id)
    {
        Console.WriteLine($"Filósofo {id} está PENSANDO...");
        Thread.Sleep(random.Next(1000, 2000)); // Pensar entre 1-2 segundos
    }

    private void TryToEat(int id)
    {
        // 1. Determinar qué tenedores necesita
        int leftFork = id;
        int rightFork = (id + 1) % numPhilosophers;
        
        // 2. Prevenir deadlock: el último filósofo toma los tenedores en orden inverso (rompe el ciclo)
        if (id == numPhilosophers - 1)
        {
            (leftFork, rightFork) = (rightFork, leftFork);
        }

        Console.WriteLine($"Filósofo {id} quiere comer - buscando tenedores {leftFork} y {rightFork}");

        // 3. Intentar tomar el primer tenedor
        forks[leftFork].WaitOne();
        Console.WriteLine($"Filósofo {id} tomó el tenedor {leftFork}");

        // 4. Intentar tomar el segundo tenedor
        forks[rightFork].WaitOne();
        Console.WriteLine($"Filósofo {id} tomó el tenedor {rightFork}");

        // 5. Comer
        Eat(id);

        counter[id]++;
        Console.WriteLine($"Filósofo {id} ha comido {counter[id]} veces");

        // 6. Liberar tenedores
        forks[rightFork].Release();
        Console.WriteLine($"Filósofo {id} liberó el tenedor {rightFork}");
        
        forks[leftFork].Release();
        Console.WriteLine($"Filósofo {id} liberó el tenedor {leftFork}");
    }

    private void Eat(int id)
    {
        Console.WriteLine($"Filósofo {id} está COMIENDO");
        Thread.Sleep(random.Next(1000, 2000)); // Comer entre 1-2 segundos
        Console.WriteLine($"Filósofo {id} terminó de comer");
    }

    /// <summary>
    /// Libera los recursos de los semáforos al finalizar la simulación.
    /// Es importante llamar a este método para evitar fugas de memoria.
    /// </summary>
    public void Dispose()
    {
        foreach (var fork in forks)
        {
            fork?.Dispose();
        }
    }
}

// Programa principal
class Program
{
    static async Task Main(string[] args)
    {
        Console.Write("Número de filósofos (default 5): ");
        var numInput = Console.ReadLine();
        int numPhilosophers = string.IsNullOrEmpty(numInput) ? 5 : int.Parse(numInput);

        Console.Write("Veces que debe comer cada filósofo (default 3): ");
        var numMeals = Console.ReadLine();
        int target = string.IsNullOrEmpty(numMeals) ? 3 : int.Parse(numMeals);

        try
        {
            var simulation = new DiningPhilosophers(numPhilosophers);
            await simulation.StartDining(target);
            simulation.Dispose();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }

        Console.WriteLine("\nPresiona cualquier tecla para salir...");
        Console.ReadKey();
    }
}