#include <iostream>

int main()
{
  int x = 42;
  int sum = 0;

  for (int i = 0; i < 10; i++) {
    int x = i;
    std::cout << "x: " << x << '\n'; // prints values of i from 0 to 9
    sum += x;
  }

  std::cout << "sum: " << sum << '\n'; // prints 45
  std::cout << "x:   " << x   << '\n'; // prints 42

  return 0;
}

/*
x: 0   
x: 1   
x: 2   
x: 3   
x: 4   
x: 5   
x: 6   
x: 7   
x: 8   
x: 9   
sum: 45
x:   42
*/