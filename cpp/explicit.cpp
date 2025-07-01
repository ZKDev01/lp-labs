
class Persona_NoExplicit {
int edad;
public:
    Persona_NoExplicit(int edad): edad(edad) { } // Permite conversión implícita
};

class Persona_Explicit {
int edad;
public:
    explicit Persona_Explicit(int edad): edad(edad) { } // Previene conversión implícita
};

void procesar(Persona_NoExplicit p) { /*...*/ }

void procesar(Persona_Explicit p) { /*...*/ } 

int main() {
    // casos problemáticos
    Persona_NoExplicit e1 = 25;
    procesar(30);
    Persona_NoExplicit e2 = 3.14;  

    /*
    No ocurre ningún error pero implica que la clase se use de forma equivocada
    */

    // ahora es necesario conversión explícita
    Persona_Explicit e3 = Persona_Explicit(25);
    //Persona_Explicit e4 = 25; // Error: no suitable constructor exists to convert from "int" to "Persona_Explicit"
    Persona_Explicit e5(25);
    
    // si se comenta void procesar(Persona_NoExplicit p) la siguiente línea da error
    //procesar(30); // Error: no suitable constructor exists to convert from "int" to "Persona_Explicit"
    
    procesar(Persona_Explicit(30));   

    /*
    Permite mayor seguridad a la hora de usar las clases
    */
}