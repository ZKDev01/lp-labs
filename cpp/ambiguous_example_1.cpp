#include <iostream>
using namespace std;

// Primer clase base
class Musico {
public:
    void tocar() {
        cout << "Tocando música..." << endl;
    }
    
    void practicar() {
        cout << "Practicando música" << endl;
    }
    
    virtual void presentarse() {
        cout << "Soy un músico" << endl;
    }
};

// Segunda clase base
class Deportista {
public:
    void tocar() {  // Mismo nombre que en Musico - CAUSA AMBIGÜEDAD
        cout << "Tocando el balón..." << endl;
    }
    
    void practicar() {  // Mismo nombre que en Musico - CAUSA AMBIGÜEDAD
        cout << "Practicando deporte" << endl;
    }
    
    virtual void presentarse() {
        cout << "Soy un deportista" << endl;
    }
    
    void entrenar() {
        cout << "Entrenando duro" << endl;
    }
};

// Clase con herencia múltiple ambigua
class PersonaCompleta : public Musico, public Deportista {
public:
    // Solución 1: Resolver ambigüedad mediante scope resolution
    void tocarMusica() {
        Musico::tocar();  // Llama específicamente al método de Musico
    }
    
    void tocarBalon() {
        Deportista::tocar();  // Llama específicamente al método de Deportista
    }
    
    // Solución 2: Sobrescribir el método ambiguo
    void practicar() {
        cout << "Practicando tanto música como deporte:" << endl;
        Musico::practicar();
        Deportista::practicar();
    }
    
    // Solución 3: Implementar método virtual ambiguo
    void presentarse() override {
        cout << "Soy una persona completa que es:" << endl;
        cout << "- ";
        Musico::presentarse();
        cout << "- ";
        Deportista::presentarse();
    }
    
    // Método que demuestra el uso de ambas capacidades
    void diaCompleto() {
        cout << "\n=== Un día en la vida ===" << endl;
        cout << "Por la mañana:" << endl;
        tocarMusica();
        Musico::practicar();
        
        cout << "\nPor la tarde:" << endl;
        tocarBalon();
        entrenar();
        
        cout << "\nPor la noche:" << endl;
        practicar();  // Usa la versión sobrescrita
    }
};

// Función que demuestra el manejo de ambigüedad
void demostrarAmbiguedad() {
    PersonaCompleta persona;
    
    cout << "=== Presentación ===" << endl;
    persona.presentarse();
    
    // Estas líneas causarían error de compilación por ambigüedad:
    // persona.tocar();      // ERROR: ambiguo
    // persona.Musico::practicar(); // OK: resolución explícita
    
    cout << "\n=== Métodos sin ambigüedad ===" << endl;
    persona.tocarMusica();
    persona.tocarBalon();
    persona.entrenar();  // Solo existe en Deportista
    
    persona.diaCompleto();
}

int main() {
    demostrarAmbiguedad();
    return 0;
}