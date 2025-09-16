function Animal(nombre) {
  this.nombre = nombre;
  this.tipo = 'animal';
}

Animal.prototype.comer = function() {
  return `${this.nombre} está comiendo`;
};

function Mamifero(nombre, tipoSangre) {
  Animal.call(this, nombre);
  this.tipoSangre = tipoSangre || 'caliente';
  this.tienePelo = true;
}

// Establecer herencia
Mamifero.prototype = Object.create(Animal.prototype);
Mamifero.prototype.constructor = Mamifero;

Mamifero.prototype.amamantar = function() {
  return `${this.nombre} está amamantando a sus crías`;
};

function Perro(nombre, raza) {
  Mamifero.call(this, nombre);
  this.raza = raza || 'canino';
}

// Establecer herencia
Perro.prototype = Object.create(Mamifero.prototype);
Perro.prototype.constructor = Perro;

Perro.prototype.ladrar = function() {
  return `${this.nombre} está ladrando: ¡Guau!`;
};

const miPerro = new Perro('Max', 'Labrador');
console.log(miPerro)