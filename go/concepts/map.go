package main

import "fmt"

func main() {
	//f1()
	f2()
}


func f1() {
	/*
	var a map[string]int
	a["A"] = 1           // panic: assigment to entry in nil map
	fmt.Println(a)
	*/
}

func f2() {
	var a = make(map[string]int)
	var b map[string]int

	fmt.Println(a) // map[]
	fmt.Println(b) // map[]
	fmt.Println(a == nil) // false
	fmt.Println(b == nil) // true
}
