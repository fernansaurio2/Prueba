// Fernando José Padilla Cruz - PC24039
#include <iostream>
#include <iomanip>

// =========================================================================
// 🛠️ FUNCIONES AUXILIARES (Para reemplazar <cmath>)
// =========================================================================

// 1. Función para el valor absoluto
double absoluto(double x) {
    return (x < 0) ? -x : x;
}

// 2. Función para generar un "Not a Number" (NaN) sin librerías
// Según el estándar IEEE 754, 0.0 / 0.0 genera un NaN válido.
double generar_nan() {
    double cero = 0.0;
    return cero / cero;
}

// =========================================================================
// ⚙️ MÉTODOS CERRADOS Y ABIERTOS
// =========================================================================

extern "C" {
    // Definimos un tipo para los punteros a funciones de Python
    typedef double (*FuncPtr)(double);

    // 1. Método de Bisección
    double biseccion(FuncPtr f, double a, double b, double tol, int max_iter, int* iteraciones) {
        *iteraciones = 0;
        if (f(a) * f(b) >= 0) {
            std::cerr << "El intervalo no contiene una raiz." << std::endl;
            return generar_nan();
        }
        double c = a;
        for (int i = 0; i < max_iter; ++i) {
            c = (a + b) / 2.0;
            if (f(c) == 0.0 || (b - a) / 2.0 < tol) return c;
            if (f(c) * f(a) < 0) b = c;
            else a = c;
            (*iteraciones)++;
        }
        return c;
    }

    // 2. Método de Falsa Posición
    double falsa_posicion(FuncPtr f, double a, double b, double tol, int max_iter, int* iteraciones) {
        *iteraciones = 0;
        if (f(a) * f(b) >= 0) {
            std::cerr << "El intervalo no contiene una raiz." << std::endl;
            return generar_nan();
        }
        double c = a;
        for (int i = 0; i < max_iter; ++i) {
            c = (a * f(b) - b * f(a)) / (f(b) - f(a));
            if (absoluto(f(c)) < tol) return c;
            if (f(c) * f(a) < 0) b = c;
            else a = c;
            (*iteraciones)++;
        }
        return c;
    }

    // 3. Método de Newton-Raphson (Modificado con Error Verdadero)
    // Nota: Ahora recibe tol_ea (aprox), tol_et (verdadero) y el valor real.
  double newton_raphson(FuncPtr f, FuncPtr df, double p0, double tol_ea, double tol_et, double valor_verdadero, int max_iter, int* iteraciones) {
        *iteraciones = 0;
        double p;
        double ea = 100.0;
        double et = 100.0;

        for (int i = 0; i < max_iter; ++i) {
            (*iteraciones)++;
            double fp = f(p0);
            double dfp = df(p0);

            if (dfp == 0) return generar_nan();

            p = p0 - fp / dfp;

            if (p != 0) ea = absoluto((p - p0) / p) * 100.0;
            if (valor_verdadero != 0) et = absoluto((valor_verdadero - p) / valor_verdadero) * 100.0;

            if (ea <= tol_ea && et <= tol_et) return p;
            p0 = p;
        }
        return p;
    }
    
    // 4. Método de la Secante
    double secante(FuncPtr f, double p0, double p1, double tol, int max_iter, int* iteraciones) {
        *iteraciones = 0;
        double p;
        for (int i = 0; i < max_iter; ++i) {
            double fp0 = f(p0);
            double fp1 = f(p1);
            if (fp1 - fp0 == 0) return generar_nan();
            
            p = p1 - fp1 * (p1 - p0) / (fp1 - fp0);
            if (absoluto(p - p1) < tol) return p;
            
            p0 = p1;
            p1 = p;
            (*iteraciones)++;
        }
        return p;
    }

    // 5. Método de Punto Fijo
    double punto_fijo(FuncPtr g, double p0, double tol, int max_iter, int* iteraciones) {
        *iteraciones = 0;
        double p;
        for (int i = 0; i < max_iter; ++i) {
            p = g(p0);
            if (absoluto(p - p0) < tol) return p;
            p0 = p;
            (*iteraciones)++;
        }
        return p;
    }
}