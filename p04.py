#Fernando José Padilla Cruz - PC24039
import ctypes
import matplotlib.pyplot as plt

# =========================================================================
# 🧮 FUNCIONES MATEMÁTICAS PURAS
# =========================================================================

def absoluto(valor):
    return -valor if valor < 0 else valor

# =========================================================================
# 📐 FUNCIÓN DEL PROBLEMA 04
# =========================================================================

# f(x) = x^3 - 7.2x^2 + 7.91x + 5.88
def f_py(x):
    return (x * x * x) - 7.2 * (x * x) + 7.91 * x + 5.88

# =========================================================================
# 📈 FUNCIÓN PARA EL MÉTODO GRÁFICO
# =========================================================================

def mostrar_grafica():
    print("\nAbriendo la gráfica de f(x)... (Analiza dónde cruza el cero antes de cerrarla)")
    
    # Rango de X ampliado de -2 a 8 para capturar todo el comportamiento cúbico
    x_vals = [i * 0.1 for i in range(-20, 81)] 
    y_vals = [f_py(x) for x in x_vals]
    
    plt.figure(figsize=(9, 5))
    plt.plot(x_vals, y_vals, label='$f(x) = x^3 - 7.2x^2 + 7.91x + 5.88$', color='#8e44ad', linewidth=2.5)
    
    plt.axhline(0, color='#e74c3c', linestyle='--', linewidth=1.5, label='Eje X (Raíces)')
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    
    plt.title('Problema 04 - Visualización de las 3 Raíces', fontsize=14, pad=15)
    plt.xlabel('Eje X')
    plt.ylabel('f(x)')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.show()

# =========================================================================
# 📊 LÓGICA PRINCIPAL Y SECANTE
# =========================================================================

def main():
    # 1. Mostrar la gráfica primero
    mostrar_grafica()

    # 2. Cargar la librería C++
    try:
        lib = ctypes.CDLL('./libraices.so')
    except OSError:
        print("❌ Error: No se encontró 'libraices.so'. Asegúrate de compilarla.")
        return

    # 3. Configurar Interfaz de la Secante
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)
    c_f = CMPFUNC(f_py)

    lib.secante.argtypes = [CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.secante.restype = ctypes.c_double

    # 4. Orquestador de iteraciones para obtener Ea exacto
    def resolver_secante(p0, p1):
        c_prev = p1
        tol_ea_objetivo = 0.1 # 0.1% exigido en el problema
        max_iter = 50
        
        for i in range(1, max_iter + 1):
            iter_ptr = ctypes.c_int(0)
            args = [c_f, ctypes.c_double(p0), ctypes.c_double(p1), ctypes.c_double(0.0), ctypes.c_int(i), ctypes.byref(iter_ptr)]
            c_curr = lib.secante(*args)
            
            if c_curr != 0: ea = absoluto((c_curr - c_prev) / c_curr) * 100.0
            else: ea = 0.0
                
            if ea < tol_ea_objetivo and i > 1: 
                return i, c_curr, ea
                
            c_prev = c_curr
            
        return max_iter, c_curr, ea

    # ---------------------------------------------------------------------
    # 🖨️ IMPRESIÓN DE RESULTADOS
    # ---------------------------------------------------------------------
    print("\nProblema 04 - Resultados del Método de la Secante")
    print("-" * 65)
    print(f"{'Identificador':<15} | {'Iteraciones':<12} | {'Valor (x)':<12} | {'Ea (%)':<10}")
    print("-" * 65)

    # Basado en la gráfica, vemos 3 cruces claros en el eje X.
    # Alimentamos a la Secante con valores iniciales (p0, p1) que rodeen cada raíz:
    intervalos = [
        ("Raíz 1", -1.0, 0.0), # Primer cruce, número negativo
        ("Raíz 2", 2.0, 3.0),  # Segundo cruce
        ("Raíz 3", 5.0, 6.0)   # Tercer cruce
    ]

    for nombre, p0, p1 in intervalos:
        i_sec, r_sec, ea_sec = resolver_secante(p0, p1)
        print(f"{nombre:<15} | {i_sec:<12} | {r_sec:<12.6f} | {ea_sec:<10.6f}")

    print("-" * 65)

if __name__ == "__main__":
    main()