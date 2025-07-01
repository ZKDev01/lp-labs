#include <iostream>
using namespace std;

int main() {
    int *ptr1 = new int;
    int *ptr2 = new int;
    int *ptr3 = new int;
    int avg;

    cout << "Enter three integers: ";
    cin >> *ptr1 >> *ptr2 >> *ptr3;

    avg = (*ptr1 + *ptr2 + *ptr3) / 3;
    cout << "Average: " << avg << endl;

    cout << "ptr1: " << ptr1 << endl;
    cout << "*ptr1: " << *ptr1 << endl;
    
    delete ptr1;
    delete ptr2;    
    delete ptr3;

    return 0;
}
