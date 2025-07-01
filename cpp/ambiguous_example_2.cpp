#include <iostream>
using namespace std;

class A {
public:
	void f() {
        cout << "f from A";
    }
};

class B {
public:
    void f() {
        cout << "f from B";
    }	
};

class AB: public A, public B { };

int main() {
    AB ab = AB();
    ab.A::f();  // Llama al método f de la clase A
    ab.B::f();  // Llama al método f de la clase B
    //ab.f();  // Error: no se puede llamar a f() directamente porque hay ambigüedad
    return 0;
}