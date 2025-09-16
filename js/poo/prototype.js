// ===== Métodos para Creación de Objetos
// == 1. Literales de Objeto

// objeto base
const person = {
  name: "default",
  eat: function() {
    console.log("eating ...");
  }
};

// == 2. Object.create()          (usado para simular herencia)

// student hereda de person
const student = Object.create(person)
student.study = function() {
  console.log("studing ...");
}

student.eat();    // eating ...
student.study();  // studing ... 

// == 3. Funciones Constructoras 

function BuildPerson(name) {
  this.person = Object.create(person)
  this.person.name = name
} 
const p = new BuildPerson("Daniel")

console.log(p)


