# LP Labs

Un kit de herramientas con ejemplos de código sencillos que abarcan múltiples lenguajes de programación y paradigmas. El objeto de este es apoyar el aprendizaje, la experimentación y el dominio de conceptos fundamentales de los diferentes lenguajes con ejemplos organizados y modulares. 

Este explora fundamentos desde gestión de memoria y concurrencia hasta patrones de diseño y estructuras de datos. Esta organizado por diferentes lenguajes (C++, Go, C# y Python). 

## Setup

- C#
  - Check version: `dotnet --version`
  - `dotnet new console -o <project-name>`
  - `dotnet run`
- C++
  - `g++ -o <output-name> <name>.cpp`
  - `./<output-name>`
- Python
  - `python <filename>.py`
- Go
  - `go run <filename>.go`
- JavaScript (tener instalado node.js)
  - `node <filename>.js`

## Gestión de Memoria

### C++ Smart Pointers Examples

Los ejemplos muestran características principales de cada puntero inteligente:

- `unique_ptr`:
  - *Propiedad exclusiva*: solo un `unique_ptr` puede poseer un recurso
  - *Move semantics*: se transfiere la propiedad con `std::move()`
- `shared_ptr`:
  - *Propiedad compartida*: múltiples `shared_ptr` puede referenciar el mismo objeto
  - *Contador de referencias*: `use_count()` muestra cuántas referencias existen
- `weak_ptr`:
  - *Observador*: no afecta el contador de referencias
  - *Evita ciclos*: rompe referencias circulares entre `shared_ptr`

> El ejemplo del cache al final demuestra un patrón común donde `weak_ptr` permite observar objetos sin mantenerlos vivos artificialmente

## Concurrencia y Paralelismo
- Threads y goroutines 
- Mecanismos de Sincronización: semáforos, barreras, countdowns y monitors

## Patrones de Diseño
- Singleton
- Factory
- Visitor 

