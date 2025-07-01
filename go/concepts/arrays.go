package main

import "fmt"

func main() {
	//f1()
	//f2()
	//f3()
	f4()
}

func f1() {
	var a = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	b := [...]int{9:10, 8:9, 7:8, 6:7, 5:6, 4:5, 3:4, 2:3, 1:2, 0:1}
	fmt.Println(a)	
	fmt.Println(b)
}

func f2(){
	var a = [...]string{"Hello", "World", "Go", "!"}
	fmt.Println(a)
	fmt.Println(len(a))
	// try access to 5 elements
	//a[4] = "Wow" // invalid argument: index 4 out of bounds [0:4]
}

func f3() {
	a1 := [5]int{}
	a2 := [5]int{1,2}
	a3 := [5]int{1,2,3,4,5}
	fmt.Println(a1)
	fmt.Println(a2)
	fmt.Println(a3)
}

func f4() {
	a := [...]int{}
	fmt.Println(a) // []
	fmt.Println(len(a)) // 0
}
