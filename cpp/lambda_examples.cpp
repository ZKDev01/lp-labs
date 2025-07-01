#include <iostream>

// ejemplo de paso por valor 
void f1() {
  int valor = 10;
  auto lambda = [valor]() {
    std::cout << "valor: " << valor << std::endl;
  };
  lambda();
}

// ejemplo de paso por referencia
void f2() { 
  int valor = 10;
  auto lambda = [&valor]() {
    valor++;
    std::cout << "valor: " << valor << std::endl;
  };
  lambda();
  std::cout << "valor despues de lambda: " << valor << std::endl;
}

void Execute(std::function<void()> func) {
  func();
}

void f3() {
  auto message = []() {
    std::cout << "Hi" << std::endl;
  };
  Execute(message);
  return 0;
}


class MyClass {
private:
  int value;
public:
  MyClass(int x) : value(x) { }
  void Execute() {
    auto lambda = [this]() {
      std::cout << "value: " << value << std::endl;
    };
    lambda();
  }
};

void f4() {
  MyClass obj(1);
  obj.Execute();
}

void f5() {
  auto imprimir = [](auto dato) {
    std::cout << dato << std::endl;
  };
  imprimir(5);        // Imprime un entero
  imprimir(3.14);     // Imprime un flotante
  imprimir("Hola");   // Imprime una cadena de texto
}

void f6() {
  int N = 10;
  int COUNTER = 5;
  auto lambda = [&COUNTER, N]() -> void {
    while (COUNTER != 0) {
      COUNTER = COUNTER - 1;
      //N = 2*N;
    }
  };
  lambda();
}

int main() {
  //f1();
  //f2();
  //f3();
  //f4();
  return 0;
}


