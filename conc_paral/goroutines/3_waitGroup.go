package main

import (
	"fmt"
	"sync"
	"time"
)

func process(id int, wg *sync.WaitGroup) {
	defer wg.Done() // marca esta gorrutina como completada al terminar
	
	fmt.Printf("Procesando ID: %d\n", id)
	time.Sleep(1 * time.Second) // simulación de algún trabajo
	fmt.Printf("ID %d procesado\n", id)
}

func main() {
	var wg sync.WaitGroup
	
	for i := 0; i < 10; i++ {
		wg.Add(1) // incrementa el contador del WaitGroup
		go process(i, &wg) // iniciar una gorrutina para cada ID
	}
	
	wg.Wait() // espera hasta que todas las gorrutinas terminen
	fmt.Println("Todos los procesos han finalizado")
}