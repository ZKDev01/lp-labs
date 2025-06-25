package main

import (
	"fmt"
	"time"
)

func process(id int) {
	fmt.Printf("Procesando ID: %d\n", id)
	time.Sleep(1 * time.Second) // simulación de algún trabajo
	fmt.Printf("ID %d procesado\n", id)
}

func main() {
	for i := 0; i < 10; i++ {
		go process(i) // iniciar una goroutine para cada ID
	}
	time.Sleep(1 * time.Second) // esperar la misma cantidad de segundos para que las goroutines terminen
	fmt.Println("Todos los procesos finalizados?") // no hay sincronización, por lo que puede que no todos los procesos hayan terminado

} // nota: cuando la función principal termina, todos los procesos en segundo plano se detienen, incluyendo las goroutines que aún están ejecutándose