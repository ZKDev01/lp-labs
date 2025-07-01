/**
 * Ejemplo práctico de características: inline, const, explicit
 */
#include <iostream>

using namespace std;

class Contador {
int _value;
public:
    explicit Contador(int v = 0) : _value(v) {}
    
    // Funciones const - solo lectura
    inline int obtener() const { return _value; }
    inline bool esPar() const { return _value % 2 == 0; }
    
    // Funciones no-const - modifican estado
    inline void incrementar() { _value++; }
    inline void reiniciar() { _value = 0; }
};

int main() {
    Contador contador(0); 
    for (int i = 1; i <= 100; ++i) {
        if (i % 3 == 0) continue; 
        cout << "Iteración " << i << ": " << contador.obtener() << endl;
        contador.incrementar();
    }
    return 0;
}