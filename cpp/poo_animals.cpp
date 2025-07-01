#include <iostream>
using namespace std;

// Clase base
class Animal {
public:
  Animal(string nombre) : nombre(nombre) {}
  virtual string hacerSonido() {
    return "El animal hace un sonido.";
  }
protected:
  string nombre;
};

// Clase derivada
class Perro : public Animal {
public:
  Perro(string nombre) : Animal(nombre) {}
  string hacerSonido() override {
	return "El perro ladra.";
  }
};

// Clase derivada
class Gato : public Animal {
public:
  Gato(string nombre) : Animal(nombre) {}
  string hacerSonido() override {
    return "El gato maúlla.";
  }
};

// Uso de las clases
int main() {
  Perro miPerro("Rex");
  Gato miGato("Mia");
    
  cout << miPerro.hacerSonido() << endl;  // Salida: El perro ladra.
  cout << miGato.hacerSonido() << endl;    // Salida: El gato maúlla.

  return 0;
}