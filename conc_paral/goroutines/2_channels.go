package main

import (
	"fmt"
	"time"
)

func process(id int, done chan bool) {
	fmt.Printf("Procesando ID: %d\n", id)
	time.Sleep(1 * time.Second) // simulación de algún trabajo
	fmt.Printf("ID %d procesado\n", id)
	done <- true // enviar señal que el proceso ha terminado
}

func main() {
	done := make(chan bool) // canal para sincronización
	numGoroutines := 10 // número de goroutines a iniciar
	// iniciar goroutines (procesos) con IDs del 0 al numGoroutines-1
	for i := 0; i < numGoroutines; i++ {
		go process(i, done) // iniciar una goroutine para cada ID
	}

	// esperar a que todas las goroutines terminen
	for i := 0; i < numGoroutines; i++ {
		<-done // esperar señal de cada goroutine
	}
	
	fmt.Println("Todos los procesos han finalizados")
}