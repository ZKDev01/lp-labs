package main

import "fmt"


type Persona struct {
	nombre string 
	Edad int 
	Email string 
}

func (p *Persona) CambiarEmail(nuevoEmail string) {
	p.Email = nuevoEmail
}

type Animal struct {
    Nombre string
}

func (a Animal) Dormir() {
    fmt.Printf("%s está durmiendo\n", a.Nombre)
}

type Perro struct {
    Animal // Embedding
    Raza   string
}

func (p Perro) Ladrar() {
    fmt.Printf("%s está ladrando\n", p.Nombre)
}


func main() {
	p := Persona{
		nombre:  "Daniel",
		Edad: 23,
		Email: "test@gmail.com",
	}
	fmt.Printf(p.nombre)

	perro := Perro{
		Animal: Animal{
			Nombre: "animalito",
		},
		Raza: "raza",
	}
	fmt.Printf("Perro creado")
	fmt.Printf(perro.Animal.Nombre)
}

