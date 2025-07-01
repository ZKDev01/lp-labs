#include <iostream>  
using namespace std;  

int main( )
{
    struct Persona
    {
        string name;
        int edad;
    };

    Persona p1 = { "Raimel",23 };
    cout << p1.name << p1.edad << endl;
    return 0;
}
