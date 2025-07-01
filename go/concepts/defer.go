package main

import (
	"fmt"
)

func basic_example(id int) {
	defer fmt.Printf("Proceso para ID %d finalizada\n", id) 
	square := id * 2 
	fmt.Printf("Procesando ID: %d\n", id)
	fmt.Printf("ID %d procesado\n", value)
} // cuando se usa defer, la función se ejecuta al final de la función actual, incluso si hay un return antes de que se alcance el final de la función. Esto es útil para liberar recursos o realizar limpieza.

func defer_in_for() {
	defer fmt.Println("Ejemplo de defer en un bucle for")
	for i := 0; i < 10; i++ {
		defer fmt.Printf("Iteración %d finalizada\n", i)
		fmt.Printf("Procesando iteración %d\n", i)
	}
}

func main() {
	defer_in_for()
} 