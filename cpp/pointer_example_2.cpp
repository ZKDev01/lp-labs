#include <iostream>
using namespace std;


int main()
{
    int num;
    int *ptr;
    
    cout << "Enter total number of elements: ";
    cin >> num;
    ptr = new int[num]; 
    
    cout << "Enter " << num << " integers: " << endl;
    for (int i = 0; i < num; ++i) {
        cout << "Element " << i + 1 << ": ";
        cin >> ptr[i]; 
    }

    cout << "You entered: " << endl;
    for (int i = 0; i < num; ++i) {
        cout << "Element " << i + 1 << ": " << ptr[i] << endl;
    }
    delete[] ptr; 

    return 0;
}
