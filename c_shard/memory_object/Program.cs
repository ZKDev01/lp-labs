using System;

class Program {
  static void Main() {
    /*
    test1();  
    test2();
    test3();
    test4();
    
    */
    test5();
  }


  static void test1() {
    int x = 50;
    update(x);
    Console.WriteLine(x);
  }

  static void test2() {
    Telefono telf = new Telefono(300);
     
    //modify_object(telf);
    create_new_obj(telf);
    
    Console.WriteLine(telf.Saldo);
  }

  static void test3() {
    int element = 10;
    to_process(ref element);
    Console.WriteLine(element);
  }
  static void test4() {
    int number = 10;
    int parameter = 20;
    int result = 10;
    to_complex_process(result, ref parameter, out result);
    Console.WriteLine(result);
  }
  static void test5() {
    Telefono t = new Telefono(100);
    reset(ref t);
    Console.WriteLine(t.Saldo);
  }

  
  static void update(int value) { 
    value = 100; 
  }
  static void modify_object(Telefono telf) { 
    telf.Saldo = 500; 
  }
  static void create_new_obj(Telefono telf) {
    telf = new Telefono(telf.Saldo + 100);
  }
  static void to_process(ref int value) {
    value = 2*value;
  }
  static void to_complex_process(int number, ref int parameter, out int result) {
    parameter = parameter + 1/2*number;
    result = number*parameter;
  }
  static void reset(ref Telefono t) => t = new Telefono(0);

}

public class Telefono {
  public int Saldo; 
  public Telefono(int saldo_inicial) {
    Saldo = saldo_inicial;
  }
}
