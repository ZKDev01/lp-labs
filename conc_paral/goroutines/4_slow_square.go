package main

import (
	"fmt"
	"sync"
	"time"
)

// Calcula el cuadrado con sleep de 1 segundo
func squareSlow(x int) int {
	time.Sleep(1 * time.Second)
	return x * x
}

// Función para suma lenta de cuadrados
func sumSquaresSlow(n int) int {
	fmt.Printf("Iniciando cálculo lento para N=%d\n", n)

	sum := 0
	for i := 1; i <= n; i++ {
		square := squareSlow(i)
		sum += square
		fmt.Printf("%d^2 = %d\n", i, square)
	}
	
	fmt.Printf("Resultado lento: %d\n", sum)
	return sum
}

// Función paralela con WaitGroup
func squareUsingWG(x int, wg *sync.WaitGroup, results chan<- int) {
	defer wg.Done()
	square := squareSlow(x)
	fmt.Printf("-> Goroutine (waitGroup): %d^2 = %d\n", x, square)
	results <- square
}

func sumSquareUsingWG(n int) int {
	fmt.Printf("Iniciando cálculo con WaitGroup para N=%d\n", n)
	
	var wg sync.WaitGroup
	results := make(chan int, n)
	
	// Lanzar todas las goroutines
	for i := 1; i <= n; i++ {
		wg.Add(1)
		go squareUsingWG(i, &wg, results)
	}
	
	// Esperar a que todas terminen
	wg.Wait()
	close(results)
	
	// Sumar los resultados
	sum := 0
	for square := range results {
		sum += square
	}

	fmt.Printf("Resultado (WaitGroup): %d\n", sum)
	return sum
}

// Función paralela solo con canales
func squareUsingChannels(ch <-chan int, results chan<- int) {
	for x := range ch {
		square := squareSlow(x)
		fmt.Printf("-> Goroutine: %d^2 = %d\n", x, square)
		results <- square
	}
}

func sumSquareUsingChannels(n int) int {
	fmt.Printf("Iniciando cálculo con Canales para N=%d\n", n)
	
	// n = número de goroutines 
	workers := make(chan int, n)
	results := make(chan int, n)
	
	for w := 1; w <= n; w++ {
		go squareUsingChannels(workers, results)
	}
	
	// Enviar trabajos
	for i := 1; i <= n; i++ {
		workers <- i
	}
	
	close(workers) // cerrar el canal de trabajos
	/*
		Cuando usas un canal para distribuir trabajos (como aquí), las goroutines leen del canal hasta que se cierra.
		Si no cierras el canal, las goroutines pueden quedarse esperando indefinidamente por más datos, causando un deadlock.
	*/
	
	// Recoger resultados
	sum := 0
	for i := 1; i <= n; i++ {
		square := <-results
		sum += square
	}
	
	fmt.Printf("Resultado (Canales): %d\n", sum)
	return sum
}



func showComparison(n int, timeSeq, timeWG, timeChannels time.Duration) {
	fmt.Printf("Comparación de Tiempos para N = %d\n", n)
	fmt.Printf("- Tiempo Secuencial:            %v\n",  timeSeq)
	fmt.Printf("- Tiempo Concurrente (WG):      %v\n",  timeWG)
	fmt.Printf("- Tiempo Concurrente (Canales): %v\n", timeChannels)
	fmt.Println()
}

func main() {
	var n int
	fmt.Print("Ingresa el valor de N: ")
	fmt.Scanf("%d", &n)
	
	fmt.Println()

	// Medición del tiempo para cada enfoque
	var timeSeq, timeWG, timeChannels time.Duration
	
	// 1. Secuencial
	start := time.Now()
	resultSeq := sumSquaresSlow(n)
	timeSeq = time.Since(start)
	
	fmt.Println()

	// 2. Uso de WaitGroup
	start = time.Now()
	resultWG := sumSquareUsingWG(n)
	timeWG = time.Since(start)
	
	fmt.Println()

	// 3. Uso de Canales
	start = time.Now()
	resultChannels := sumSquareUsingChannels(n)
	timeChannels = time.Since(start)
	
	fmt.Println()

	// Verificar que todos los resultados son iguales
	if resultSeq == resultWG && resultSeq == resultChannels {
		showComparison(n, timeSeq, timeWG, timeChannels)
	} else {
		fmt.Printf("ERROR: Secuencial: %d, WaitGroup: %d, Canales: %d\n\n", resultSeq, resultWG, resultChannels)
	}
}