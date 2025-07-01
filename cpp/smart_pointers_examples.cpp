#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <algorithm>

class Recurso {
public:
    std::string nombre;
    
    Recurso(const std::string& n) : nombre(n) {
        std::cout << "Creando recurso: " << nombre << std::endl;
    }
    
    ~Recurso() {
        std::cout << "Destruyendo recurso: " << nombre << std::endl;
    }
    
    void usar() {
        std::cout << "Usando recurso: " << nombre << std::endl;
    }
};

// ======================
// EJEMPLOS DE unique_ptr
// ======================
void ejemplos_unique_ptr() {
    std::cout << "\n=== EJEMPLOS unique_ptr ===\n";
    
    // 1. Creación básica
    std::unique_ptr<Recurso> ptr1 = std::make_unique<Recurso>("Recurso1");
    ptr1->usar();
    
    // 2. Transferencia de propiedad (move)
    std::unique_ptr<Recurso> ptr2 = std::move(ptr1);
    // ptr1 ahora es nullptr
    if (!ptr1) {
        std::cout << "ptr1 es nullptr despues del move\n";
    }
    ptr2->usar();
    
    // 3. unique_ptr con arrays
    std::unique_ptr<int[]> array_ptr = std::make_unique<int[]>(5);
    for (int i = 0; i < 5; ++i) {
        array_ptr[i] = i * 10;
    }
    
    // 4. Función que retorna unique_ptr
    auto crear_recurso = [](const std::string& nombre) -> std::unique_ptr<Recurso> {
        return std::make_unique<Recurso>(nombre);
    };
    
    auto recurso_nuevo = crear_recurso("RecursoFactory");
    recurso_nuevo->usar();
    
    // 5. Release y reset
    std::unique_ptr<Recurso> ptr3 = std::make_unique<Recurso>("Recurso3");
    Recurso* raw_ptr = ptr3.release(); // Libera la propiedad
    delete raw_ptr; // Ahora tenemos que eliminar manualmente
    
    ptr3.reset(new Recurso("Recurso3_Reset")); // Asigna nuevo recurso
}

// ======================
// EJEMPLOS DE shared_ptr
// ======================
void ejemplos_shared_ptr() {
    std::cout << "\n=== EJEMPLOS shared_ptr ===\n";
    
    // 1. Creación y compartición básica
    std::shared_ptr<Recurso> ptr1 = std::make_shared<Recurso>("RecursoCompartido");
    std::cout << "Contador de referencias: " << ptr1.use_count() << std::endl;
    
    {
        std::shared_ptr<Recurso> ptr2 = ptr1; // Copia, incrementa contador
        std::cout << "Contador despues de copia: " << ptr1.use_count() << std::endl;
        ptr2->usar();
    } // ptr2 sale de alcance, decrementa contador
    
    std::cout << "Contador despues de salir de alcance: " << ptr1.use_count() << std::endl;
    
    // 2. shared_ptr en contenedores
    std::vector<std::shared_ptr<Recurso>> recursos;
    auto recurso_compartido = std::make_shared<Recurso>("RecursoEnVector");
    
    recursos.push_back(recurso_compartido);
    recursos.push_back(recurso_compartido); // Mismo recurso en múltiples lugares
    
    std::cout << "Contador en vector: " << recurso_compartido.use_count() << std::endl;
    
    // 3. Custom deleter
    auto custom_deleter = [](Recurso* r) {
        std::cout << "Eliminando con deleter personalizado: " << r->nombre << std::endl;
        delete r;
    };
    
    std::shared_ptr<Recurso> ptr_custom(new Recurso("RecursoCustomDeleter"), custom_deleter);
}

// ====================
// EJEMPLOS DE weak_ptr
// ====================
class Nodo {
public:
    std::string valor;
    std::shared_ptr<Nodo> siguiente;
    std::weak_ptr<Nodo> anterior; // weak_ptr para evitar ciclos
    
    Nodo(const std::string& v) : valor(v) {
        std::cout << "Creando nodo: " << valor << std::endl;
    }
    
    ~Nodo() {
        std::cout << "Destruyendo nodo: " << valor << std::endl;
    }
};

void ejemplos_weak_ptr() {
    std::cout << "\n=== EJEMPLOS weak_ptr ===\n";
    
    // 1. Evitando referencias circulares
    auto nodo1 = std::make_shared<Nodo>("Nodo1");
    auto nodo2 = std::make_shared<Nodo>("Nodo2");
    
    nodo1->siguiente = nodo2;
    nodo2->anterior = nodo1; // weak_ptr, no incrementa contador
    
    std::cout << "Contador nodo1: " << nodo1.use_count() << std::endl;
    std::cout << "Contador nodo2: " << nodo2.use_count() << std::endl;
    
    // 2. Verificar si el objeto aún existe
    std::weak_ptr<Recurso> weak_ptr;
    
    {
        auto shared_recurso = std::make_shared<Recurso>("RecursoTemporal");
        weak_ptr = shared_recurso;
        
        if (auto locked = weak_ptr.lock()) {
            std::cout << "Objeto aún existe: ";
            locked->usar();
        }
    } // shared_recurso se destruye aquí
    
    // 3. Verificar si el objeto fue destruido
    if (weak_ptr.expired()) {
        std::cout << "El objeto ha sido destruido\n";
    }
    
    // 4. Uso seguro con lock()
    auto recurso_principal = std::make_shared<Recurso>("RecursoPrincipal");
    std::weak_ptr<Recurso> observador = recurso_principal;
    
    // Función que usa weak_ptr de forma segura
    auto usar_si_existe = [&observador]() {
        if (auto ptr = observador.lock()) {
            ptr->usar();
        } else {
            std::cout << "El recurso ya no está disponible\n";
        }
    };
    
    usar_si_existe(); // Funciona
    recurso_principal.reset(); // Libera el recurso
    usar_si_existe(); // Ya no funciona
}

// ============================================
// EJEMPLO: Cache con weak_ptr
// ============================================
class Cache {
private:
    std::vector<std::weak_ptr<Recurso>> cache;
    
public:
    void agregar(std::shared_ptr<Recurso> recurso) {
        cache.push_back(recurso);
    }
    
    void limpiar_expirados() {
        auto it = std::remove_if(cache.begin(), cache.end(),
                                [](const std::weak_ptr<Recurso>& wp) {
                                    return wp.expired();
                                });
        cache.erase(it, cache.end());
        std::cout << "Cache limpiado. Elementos restantes: " << cache.size() << std::endl;
    }
    
    void mostrar_activos() {
        std::cout << "Recursos activos en cache:\n";
        for (auto& wp : cache) {
            if (auto sp = wp.lock()) {
                std::cout << "  - " << sp->nombre << std::endl;
            }
        }
    }
};

void ejemplo_cache() {
    std::cout << "\n=== EJEMPLO CACHE CON weak_ptr ===\n";
    
    Cache cache;
    {
        auto r1 = std::make_shared<Recurso>("CacheRecurso1");
        auto r2 = std::make_shared<Recurso>("CacheRecurso2");
        
        cache.agregar(r1);
        cache.agregar(r2);
        cache.mostrar_activos();
    } // r1 y r2 salen de alcance
    
    cache.limpiar_expirados();
    cache.mostrar_activos();
}

int main() {
    ejemplos_unique_ptr();
    ejemplos_shared_ptr();
    ejemplos_weak_ptr();
    ejemplo_cache();
    return 0;
}