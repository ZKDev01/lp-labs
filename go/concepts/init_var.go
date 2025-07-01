package main

func initVar() {
	/* alternative hello world printer */
	var a string
	println(a)
	var b int
	println(b)
	var c bool
	println(c)
}

func multVar() {
	a, b := 1, "Hola"
	println(a)
	println(b)
}

func main() {
	/* alternative hello world printer */
	multVar()
}