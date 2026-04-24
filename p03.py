#Fernando José Padilla Cruz - PC24039
import ctypes
import matplotlib.pyplot as plt  # Se usa ÚNICAMENTE para la interfaz visual (el ploteo)

# =========================================================================
# 🧮 FUNCIONES MATEMÁTICAS PURAS (Sin Numpy ni Math)
# =========================================================================

def absoluto(valor):
    return -valor if valor < 0 else valor

def mi_sqrt(S):
    if S <= 0: return 0.0
    x = S / 2.0
    for _ in range(25): 
        x = 0.5 * (x + S / x)
    return x

# =========================================================================
# 📐 FUNCIONES DEL PROBLEMA 03
# =========================================================================

def f_py(x):
    return -0.9 * (x * x) + 1.7 * x + 2.5

def df_py(x):
    return -1.8 * x + 1.7

def g_py(x):
    try:
        adentro = (1.7 * x + 2.5) / 0.9
        return mi_sqrt(adentro)
    except:
        return float('nan')

# =========================================================================
# 📈 FUNCIÓN PARA EL MÉTODO GRÁFICO
# =========================================================================

def mostrar_grafica():
    # Generamos valores de X desde -2.0 hasta 4.0 usando solo Python puro (sin numpy)
    x_vals = [i * 0.1 for i in range(-20, 41)] 
    y_vals = [f_py(x) for x in x_vals]
    
    plt.figure(figsize=(9, 5))
    plt.plot(x_vals, y_vals, label='$f(x) = -0.9x^2 + 1.7x + 2.5$', color='#2980b9', linewidth=2.5)
    
    # Líneas de los ejes para ubicar el cero fácilmente
    plt.axhline(0, color='#e74c3c', linestyle='--', linewidth=1.5, label='Eje X (Raíces)')
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    
    # Títulos y diseño
    plt.title('Problema 03 - Método Gráfico', fontsize=14, pad=15)
    plt.xlabel('Eje X')
    plt.ylabel('f(x)')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    
    # Mostrar la ventana interactiva
    plt.show()

# =========================================================================
# 📊 LÓGICA PRINCIPAL Y PLOTEO DE LA TABLA 2
# =========================================================================

def main():
    # 2. Cargar la librería C++
    try:
        lib = ctypes.CDLL('./libraices.so')
    except OSError:
        print("❌ Error: No se encontró 'libraices.so'.")
        return

    # 3. Configurar Interfaces
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)
    c_f  = CMPFUNC(f_py)
    c_df = CMPFUNC(df_py)
    c_g  = CMPFUNC(g_py)

    lib.punto_fijo.argtypes = [CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.punto_fijo.restype = ctypes.c_double

    lib.newton_raphson.argtypes = [CMPFUNC, CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.newton_raphson.restype = ctypes.c_double

    # 4. Orquestador
    def resolver_metodo(metodo, p0, is_newton=False):
        c_prev = 0.0
        tol_ea_objetivo = 0.1 # 0.1 %
        max_iter = 25
        
        for i in range(1, max_iter + 1):
            iter_ptr = ctypes.c_int(0)
            if is_newton:
                args = [c_f, c_df, ctypes.c_double(p0), ctypes.c_double(0.0), ctypes.c_double(100.0), ctypes.c_double(0.0), ctypes.c_int(i), ctypes.byref(iter_ptr)]
            else:
                args = [c_g, ctypes.c_double(p0), ctypes.c_double(0.0), ctypes.c_int(i), ctypes.byref(iter_ptr)]
                
            c_curr = metodo(*args)
            
            if c_curr != 0: ea = absoluto((c_curr - c_prev) / c_curr) * 100.0
            else: ea = 0.0
                
            if ea < tol_ea_objetivo and i > 1: return i, c_curr, ea
            c_prev = c_curr
            
        return max_iter, c_curr, ea

    # ---------------------------------------------------------------------
    # 🖨️ IMPRESIÓN DE LA TABLA 2
    # ---------------------------------------------------------------------
    print("\nProblema 03 - Tabla 2. Resumen")
    print("-" * 65)
    print(f"{'Método de cálculo:':<20} | {'Iteración':<10} | {'Valor':<12} | {'Ea (%)':<10}")
    print("-" * 65)

    # De ver la gráfica anterior, sabemos que corta el eje X cerca del 2.8, usaremos 3.0
    p0_inicial = 3.0

    print(f"{'1 Gráfico':<20} | {'N/A':<10} | {f'~{p0_inicial}':<12} | {'N/A':<10}")

    i_pf, r_pf, ea_pf = resolver_metodo(lib.punto_fijo, p0_inicial, is_newton=False)
    print(f"{'2 Punto fijo':<20} | {i_pf:<10} | {r_pf:<12.6f} | {ea_pf:<10.6f}")

    i_nr, r_nr, ea_nr = resolver_metodo(lib.newton_raphson, p0_inicial, is_newton=True)
    print(f"{'3 Newton Raphson':<20} | {i_nr:<10} | {r_nr:<12.6f} | {ea_nr:<10.6f}")

    print("-" * 65)

    mostrar_grafica()

if __name__ == "__main__":
    main()