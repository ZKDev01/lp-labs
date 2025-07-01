package main

import "fmt"

func main() {
	var person Person
	
	person.name = "Daniel"
	person.age = 23
	
	fmt.Println(person) // {Daniel 23}
	
	Printer_Person(person)
	/*
	Name: Daniel
	Age: 23
	*/
	

	fmt.Println("OK!")
}

func Printer_Person(person Person) {
	fmt.Println("Name:", person.name)
	fmt.Println("Age:", person.age)
}

type Person struct {
	name string
	age int 
}
