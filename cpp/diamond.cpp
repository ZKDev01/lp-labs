#include <iostream>
#include <string>
#include <vector>
#include <memory>
using namespace std;

class Person {
protected:
  string name;
  int age; 
public: 
  Person(string name, int age) : name(name), age(age) { }

  virtual void showInfo() {
    cout << "Person(name: " << name << ", age: " << age << ")" << endl;
  }

  string getName() const { return name; }
  int getAge() const { return age; }

  virtual ~Person() {
    cout << "Person " << name << " has been eliminated" << endl;
  }
};

class Teacher : public virtual Person {
protected:
  string subject;
public: 
  Teacher(string name, int age, string subject) : Person(name, age), subject(subject) { }

  void showInfo() {
    cout << "Teacher(name: " << name << ", age: " << age << ")" << endl;
    cout << "  Teaching " << subject << endl;
  }
};

class Student : public virtual Person {
protected:
  string career;
public: 
  Student(string name, int age, string career) : Person(name, age), career(career) { }

  void showInfo() {
    cout << "Student(name: " << name << ", age: " << age << ")" << endl;
    cout << "  Studying " << career << endl;
  }
};

class TeacherStudent : public Teacher, public Student {
public:
  TeacherStudent(string name, int age, string subject, string career) : Person(name, age), Teacher(name, age, subject), Student(name, age, career) { }
  
  void showInfo() {
    cout << "TeacherStudent(name: " << name << ", age: " << age << ")" << endl;
    cout << "  Teaching " << subject << endl;
    cout << "     and   " << endl;
    cout << "  Studying " << career << endl;
  }
  
};


// Si se comenta showInfo de TeacherStudent se obtiene: request for member 'showInfo' is ambiguous
void test() {
  TeacherStudent teacherStudent1("Daniel", 23, "Lenguajes de Programacion", "Ciencias de la Computacion");
  teacherStudent1.showInfo();
}

int main() {
  test();
  return 0;
}