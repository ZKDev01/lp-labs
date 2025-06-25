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

// Calcula la suma de una lista de enteros
func sumArray(array []int) int {
 	sum := 0
 	for _, num := range array {
		sum += num
 	}
 	return sum
}

// Calcula el máximo de una lista de enteros
func maxArray(array []int) int {
	if len(array) == 0 {
		return 0
	}
	max := array[0]
	for _, num := range array[1:] {
		if num > max {
			max = num
		}
	}
	return max
}

func main() {
	var n int
	fmt.Print("Ingresa el valor de N: ")
	fmt.Scanf("%d", &n)
	
	var wg1 sync.WaitGroup
  var wg2 sync.WaitGroup
	var mutex sync.Mutex
	newArray := make([]int, 0, n)	
	
	// creación de una lista de cuadrados de números del 1 al N usando waitGroup
	for i := 1; i <= n; i++ {
		wg1.Add(1)
		go func(num int) {
			defer wg1.Done()
			result := squareSlow(num)

			mutex.Lock() // Bloquear acceso a newArray, evitando condiciones de carrera
			newArray = append(newArray, result)
	 		mutex.Unlock()
		}(i)
	}
	wg1.Wait() // Esperar a que todas las goroutines terminen
	fmt.Println("Nueva lista: %v\n", newArray)
	
	// funciones sobre la nueva lista 
	var sum, max int 
	wg2.Add(2) 
	go func() {
		defer wg2.Done()
		sum = sumArray(newArray)
		fmt.Printf("Suma de la lista: %d\n", sum)
	}()
	go func() {
		defer wg2.Done()
		max = maxArray(newArray)
		fmt.Printf("Máximo de la lista: %d\n", max)
	}()

	wg2.Wait() // Esperar a que ambas goroutines terminen
}