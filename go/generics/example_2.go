package main

import "fmt"

func main() {
	f1()
}

func f1() {
	ints := map[string]int64 {
		"first":  34,
		"second": 12,
	}
	floats := map[string]float64 {
		"first":  34.9,
		"second": 25.1,
	}
	
	fmt.Printf("Generic Sums: %v and %v\n",
		SumT(ints),
		SumT(floats))
}

type Number interface {
	int64 | float64 
}

// comparable => interface
func SumT[ K comparable, V Number ](m map[K]V) V {
	var s V 
	for _,v := range m {
		s += v
	}
	return s
}
