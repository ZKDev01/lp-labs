package main

import (
	"fmt"
	"sync"
	"time"
)


/*
==== Ejemplo de uso de Mutex en Go ===
= usa mutex.Lock() y mutex.Unlock() para proteger el acceso a una variable compartida
= Lock() bloquea el mutex, solo una goroutine puede continuar 
= Unlock() libera el mutex, permitiendo que otras goroutines accedan
= Se usa defer para asegurar que el mutex se desbloquee al salir de la función
*/


// Contador seguro usando mutex
type SafeCounter struct {
	mu    sync.Mutex
	value int
}

// Incrementa el contador de forma segura
func (c *SafeCounter) Increment() {
	c.mu.Lock()         // Bloquea el acceso
	defer c.mu.Unlock() // Desbloquea al salir de la función
	c.value++
}

// Obtiene el valor actual de forma segura
func (c *SafeCounter) GetValue() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// Función que simula trabajo y incrementa el contador
func worker(id int, counter *SafeCounter, wg *sync.WaitGroup) {
	defer wg.Done()
	
	for i := 0; i < 1000; i++ {
		counter.Increment()
		time.Sleep(time.Microsecond) // Simula algo de trabajo,
	}
	
	fmt.Printf("Worker %d terminado\n", id)
}




// Ejemplo de contador SIN mutex (para mostrar el problema)
type UnsafeCounter struct {
	value int
}

func (c *UnsafeCounter) Increment() {
	// Sin mutex - operación no atómica
	c.value++
}

func (c *UnsafeCounter) GetValue() int {
	return c.value
}

func unsafeWorker(id int, counter *UnsafeCounter, wg *sync.WaitGroup) {
	defer wg.Done()
	
	for i := 0; i < 1000; i++ {
		counter.Increment()
	}
}

func unsafeCounterExample() {
	unsafeCounter := &UnsafeCounter{}
	var wg sync.WaitGroup
	
	numWorkers := 5
	
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go unsafeWorker(i, unsafeCounter, &wg)
	}
	
	wg.Wait()
	
	fmt.Printf("Contador sin mutex (resultado impredecible): %d\n", unsafeCounter.GetValue())
	fmt.Printf("El resultado puede ser menor a %d debido a race conditions\n", numWorkers*1000)
}





func main() {
	fmt.Println("Ejemplo de Mutex en Go")
	fmt.Println("======================")
	
	// Crear un contador seguro
	counter := &SafeCounter{}
	
	// WaitGroup para esperar a que terminen todas las goroutines
	var wg sync.WaitGroup
	
	// Número de workers
	numWorkers := 5
	
	fmt.Printf("Iniciando %d workers, cada uno incrementará 1000 veces\n", numWorkers)
	fmt.Printf("Valor esperado: %d\n\n", numWorkers*1000)
	
	// Iniciar workers
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go worker(i, counter, &wg)
	}
	
	// Esperar a que terminen todos los workers
	wg.Wait()
	
	fmt.Printf("\nTodos los workers han terminado\n")
	fmt.Printf("Valor final del contador: %d\n", counter.GetValue())
	
	// Ejemplo adicional: mostrar problema sin mutex
	fmt.Println("\n--- Comparación sin mutex ---")
	unsafeCounterExample()
}
