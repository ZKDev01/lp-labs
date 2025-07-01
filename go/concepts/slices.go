package main

import "fmt"

func main() {
	//f1()
	f2()
}

func f1() {
	var s1 = []int{0}
	var s2 = append(s1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
	fmt.Println(s1)  // [0]
	fmt.Println(s2)  // [0 1 2 3 4 5 6 7 8 9 10]
	s1[0] = 1000
	fmt.Println(s1)  // [1000]
	fmt.Println(s2)  // [0 1 2 3 4 5 6 7 8 9 10]

	var s3 = append(s1,s2...)
	fmt.Println(s3)  // [1000 0 1 2 3 4 5 6 7 8 9 10]
}

func f2() {
	var s1 = []int {1,2,3,4,5,6,7,8,9}
	fmt.Println(len(s1)/2)
	var s2 = s1[0:len(s1)/2]
	fmt.Println(s2) // [ 1 2 3 4 5 ]
	s1[2] = 1000
	fmt.Println(s2) // [ 1 2 1000 4 5 ]
	s2 = append(s2, 9999)
	fmt.Println(s1) // [ 1 2 1000 4 5 9999 7 8 9 0 ]
}

func f3() {
	var s1 = []int {1,2,3}
	var s2 = []int {4,5,6}
	fmt.Println(s1)
	fmt.Println(s2)
	//fmt.Println(s1 + s2)
}

func f4() {
	var s1 = []int {1,2,3,4,5,6,7,8,9}
	//var lenght float32 = len(s1)
	fmt.Println(s1)
	//fmt.Println(lenght)
}