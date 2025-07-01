using System;

class Program {
  static void Main() {
    test1();  // Calling test1 method
  }


  static void test1() {
    DNT obj1 = new DNT();

    // Calling the Display method to access the class level variable
    obj1 .Display();
  }
}





class Example {  
  int a = 10;    // Class level variable with class level scope

  public void Display() {
    Console.WriteLine(a);   // Accessing class level variable
  }
}

class Example_error { // from here class level scope starts

  public void Display() {   // from here method level scope starts 
    int m = 5;                // this variable has method level scope
    Console.WriteLine(m);     // accessing method level variable 
  } // here method level scope ends
  
  public void Display_error() {
    // it will give compile time error as
    // you are trying to access the local variable of method Display()
    Console.WriteLine(m);
  }
}

class Example_loop {

  public void Display() {
    int i = 0;                      // this variable has method level scope
    for (i = 0; i < 5; i++) {
      Console.WriteLine(i);         // accessing method level variable
    }
    Console.WriteLine(i);

    for (int j = 0; j < 5; j++) {
      Console.WriteLine(j);         // here j is block level variable. its only accessible inside this for loop
    }
    
    // this will give error as block level variable can't be accessed outside the block
    Console.WriteLine(j);
  }
}





// C# code to illustrate the Block Level scope of variables
using System;

// declaring a Class
class DNT

{ // from here class level scope starts

  // declaring a method
  public void display()

  { // from here method level scope starts
    int i = 0;
    for (i = 0; i < 4; i++) {
      Console.WriteLine(i);
    }

    Console.WriteLine(i);
    // here j is block level variable
    // it is only accessible inside this for loop
    for (int j = 0; j < 5; j++) {
      // accessing block level variable
      Console.WriteLine(j);
    }

    // this will give error as block level variable can't be accessed outside the block
    Console.WriteLine(j);

  } // here method level scope ends
} // here class level scope ends
