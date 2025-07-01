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
		SumT[string,int64](ints),
		SumT[string,float64](floats))		
	
	fmt.Printf("Generic Sums: %v and %v\n",
		SumT(ints),
		SumT(floats))
}

func SumT[ K comparable, V int64 | float64 ](m map[K]V) V {
	var s V 
	for _,v := range m {
		s += v
	}
	return s
}


