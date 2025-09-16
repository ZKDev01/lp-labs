// ===== Herencia simple con Prototipos
// == 1. Usando Object.create()

// objeto base
const Animal = {
  type: "animal",
  eat: function() {
    return `${this.name} is eating ...`;
  },
  sleep: function() {
    return `${this.name} is sleeping ...`;
  }
};

// objeto hijo
const Dog = Object.create(Animal);
Dog.name = "Hope"
Dog.type = 'husky';

console.log(Animal)
console.log(Dog)
console.log(Dog.sleep())
