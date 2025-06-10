#include <iostream>
#include <vector>
#include <memory>

using namespace std;

/**
 * TreeNode
 *      Interfaz base para nodos del árbol
 */
class TreeNode {
public:
    virtual ~TreeNode() = default;
    virtual void accept(class Visitor& visitor) const = 0;
};

/**
 * Visitor
 *      Interfaz Visitor (Visitante)
 */
class Visitor { 
public: 
    virtual void visitNumber(const class NumberNode& node) = 0;
    virtual void visitAdd(const class AddNode& node) = 0;
};


/**
 * SpecificClasses
 * - NumberNode -> nodo para números
 * - AddNode    -> nodo para el operador + 
 */
class NumberNode : public TreeNode {
    int _value;
public: 
    explicit NumberNode(int _value) : _value(_value) { }
    int value() const { return _value; }

    void accept(Visitor& visitor) const override {
        visitor.visitNumber(*this);
    }
};

class AddNode : public TreeNode {
    unique_ptr<TreeNode> _left;
    unique_ptr<TreeNode> _right;
public:
    AddNode(unique_ptr<TreeNode> _left, unique_ptr<TreeNode> _right) 
        : _left(move(_left)), _right(move(_right)) { }
    
    const TreeNode& get_left() const { return *_left; }
    const TreeNode& get_right() const { return *_right; }

    void accept(Visitor& visitor) const override {
        visitor.visitAdd(*this);
    }
    
};


/**
 * SpecificVisitor 
 * - CalculateVisitor -> cálculo de resultados
 */
class CalculateVisitor: public Visitor {
    int _result = 0;
public: 
    int result() const { return _result; }

    void visitNumber(const NumberNode& node) override {
        _result = node.value();
    }
    void visitAdd(const AddNode& node) override {
        // calcular subárbol izquierdo
        CalculateVisitor _leftVisitor;
        node.get_left().accept(_leftVisitor);

        // calcular subárbol derecho
        CalculateVisitor _rightVisitor;
        node.get_right().accept(_rightVisitor);

        // combinar resultados
        _result = _leftVisitor.result() + _rightVisitor.result();
    }
};




/**
 * Test
 * - test_1: (5 + 2) + (7 + (4 + 2))
*/
void test_1() {
    // construir árbol: (5 + 2) + (7 + (4 + 2))
    auto expression = make_unique<AddNode>(
        make_unique<AddNode>(
            make_unique<NumberNode>(5),
            make_unique<NumberNode>(2)
        ),
        make_unique<AddNode>(
            make_unique<NumberNode>(7),
            make_unique<AddNode>(
                make_unique<NumberNode>(4),
                make_unique<NumberNode>(2)
            )
        )
    );

    CalculateVisitor calculator;
    expression->accept(calculator);

    cout << "Result: " << calculator.result();
}


int main() {
    test_1();
    return 0;
}


