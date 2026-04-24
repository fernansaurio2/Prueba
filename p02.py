import ctypes

# =========================================================================
# 🧮 FUNCIONES MATEMÁTICAS PURAS (Sin importar 'math')
# =========================================================================

def absoluto(valor):
    return -valor if valor < 0 else valor

# 1. Raíz Cuadrada por Método de Newton (x_new = 0.5 * (x_old + S / x_old))
# f(x) = x^2 - S  =>  x_new = 0.5 * (x_old + S / x_old)
def mi_sqrt(S):
    if S <= 0: return 0.0
    x = S / 2.0 # Semilla inicial
    for _ in range(25): # 25 iteraciones bastan para precisión doble
        x = 0.5 * (x + S / x)
    return x

# 2. Función Exponencial (e^x) por Serie de Taylor
def mi_exp(x):
    suma = 1.0
    term = 1.0
    for i in range(1, 35):
        term *= x / i
        suma += term
        if absoluto(term) < 1e-12: break
    return suma

# 3. Coseno por Serie de Taylor
def mi_cos(x):
    suma = 1.0
    term = 1.0
    x2 = x * x
    for i in range(1, 25):
        term *= -x2 / ((2 * i) * (2 * i - 1))
        suma += term
        if absoluto(term) < 1e-12: break
    return suma

# 4. Seno por Serie de Taylor (necesario para la derivada)
def mi_sin(x):
    suma = x
    term = x
    x2 = x * x
    for i in range(1, 25):
        term *= -x2 / ((2 * i) * (2 * i + 1))
        suma += term
        if absoluto(term) < 1e-12: break
    return suma

# =========================================================================
# 📐 FUNCIONES DEL CIRCUITO RLC
# =========================================================================

def f_py(R):
    try:
        exp_term = mi_exp(-0.005 * R)
        cos_term = mi_cos(0.05 * mi_sqrt(2000.0 - 0.01 * R * R))
        return exp_term * cos_term - 0.01
    except Exception:
        return float('nan')

def df_py(R):
    try:
        raiz = mi_sqrt(2000.0 - 0.01 * R * R)
        exp_term = mi_exp(-0.005 * R)
        v = 0.05 * raiz
        
        term1 = -0.005 * mi_cos(v)
        term2 = (0.0005 * R * mi_sin(v)) / raiz
        
        return exp_term * (term1 + term2)
    except Exception:
        return float('nan')

def main():
    print("Problema 02 - Análisis de Circuito RLC (100% Puro, Cero Librerías Matemáticas)")
    print("=" * 75)

    try:
        lib = ctypes.CDLL('./libraices.so')
    except OSError:
        print("❌ Error: No se encontró 'libraices.so'.")
        return

    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)
    c_f = CMPFUNC(f_py)
    c_df = CMPFUNC(df_py)

    lib.biseccion.argtypes = [CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.biseccion.restype = ctypes.c_double

    lib.falsa_posicion.argtypes = [CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.falsa_posicion.restype = ctypes.c_double

    # NOTA: Agregamos el nuevo argumento 'imprimir_tabla' (ctypes.c_int) al final
    lib.newton_raphson.argtypes = [CMPFUNC, CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    lib.newton_raphson.restype = ctypes.c_double

    lib.secante.argtypes = [CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.secante.restype = ctypes.c_double

    a, b = 320.0, 330.0
    tol = 0.0001
    max_iter = 50
    iter_ptr = ctypes.c_int(0)

    print("\n📊 RESULTADOS DE LA LIBRERÍA C++ (Para llenar la Tabla 1)\n")
    print(f"{'Método':<18} | {'Iteración':<10} | {'Valor (R)':<12}")
    print("-" * 45)

    r_bis = lib.biseccion(c_f, ctypes.c_double(a), ctypes.c_double(b), ctypes.c_double(tol), ctypes.c_int(max_iter), ctypes.byref(iter_ptr))
    print(f"{'2. Bisección':<18} | {iter_ptr.value:<10} | {r_bis:.5f} Ω")

    r_fp = lib.falsa_posicion(c_f, ctypes.c_double(a), ctypes.c_double(b), ctypes.c_double(tol), ctypes.c_int(max_iter), ctypes.byref(iter_ptr))
    print(f"{'3. Posición Falsa':<18} | {iter_ptr.value:<10} | {r_fp:.5f} Ω")

    # Mandamos un '0' al final para SILENCIAR la tabla de C++
    r_nr = lib.newton_raphson(c_f, c_df, ctypes.c_double(325.0), ctypes.c_double(tol), ctypes.c_double(100.0), ctypes.c_double(0.0), ctypes.c_int(max_iter), ctypes.byref(iter_ptr), ctypes.c_int(0))
    print(f"{'4. Newton-Raphson':<18} | {iter_ptr.value:<10} | {r_nr:.5f} Ω")

    r_sec = lib.secante(c_f, ctypes.c_double(a), ctypes.c_double(b), ctypes.c_double(tol), ctypes.c_int(max_iter), ctypes.byref(iter_ptr))
    print(f"{'5. Secante':<18} | {iter_ptr.value:<10} | {r_sec:.5f} Ω")

    # Demostración
    print("\n" + "=" * 60)
    print("🔍 DEMOSTRACIÓN: Bisección a las 20 iteraciones (Vía C++)")
    print("=" * 60)
    
    raiz_19 = lib.biseccion(c_f, ctypes.c_double(a), ctypes.c_double(b), ctypes.c_double(0.0), ctypes.c_int(19), ctypes.byref(iter_ptr))
    raiz_20 = lib.biseccion(c_f, ctypes.c_double(a), ctypes.c_double(b), ctypes.c_double(0.0), ctypes.c_int(20), ctypes.byref(iter_ptr))
    
    error_aprox_20 = absoluto((raiz_20 - raiz_19) / raiz_20) * 100.0
    
    print(f"Raíz en iteración 19 (desde .so) : {raiz_19:.6f} Ω")
    print(f"Raíz en iteración 20 (desde .so) : {raiz_20:.6f} Ω")
    print(f"Error Aproximado (Ea) calculado  : {error_aprox_20:.6f} %\n")

if __name__ == "__main__":
    main()