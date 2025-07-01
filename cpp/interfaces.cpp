// Simulación de Interfaces en C++ usando herencia

class IShape {
public:
    virtual ~IShape() = default;        // Destructor virtual
    virtual void draw() const = 0;      // Método puro, obliga a implementar
    virtual double area() const = 0;    // Otro método puro
};


class Circle : public IShape {
    double radius_;
public:
    Circle(double r) : radius_(r) {}
    void draw() const override {
        // implementación específica
    }
    double area() const override {
        return 3.14159 * radius_ * radius_;
    }
};
