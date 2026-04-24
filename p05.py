#Fernando José Padilla Cruz - PC24039
import ctypes
import matplotlib.pyplot as plt

# =========================================================================
# 🧮 FUNCIONES MATEMÁTICAS PURAS
# =========================================================================

def absoluto(valor):
    return -valor if valor < 0 else valor

MI_PI = 3.141592653589793

# =========================================================================
# 📐 FUNCIONES DEL PROBLEMA 05 (Tanque Esférico)
# =========================================================================

# f(h) = pi * h^2 * (9 - h) / 3 - 30
def f_py(h):
    return MI_PI * (h * h) * (9.0 - h) / 3.0 - 30.0

# f'(h) = pi * (6h - h^2)
def df_py(h):
    return MI_PI * (6.0 * h - (h * h))

# =========================================================================
# 📈 FUNCIÓN GRÁFICA Y ANÁLISIS FÍSICO
# =========================================================================

def mostrar_grafica():
    print("Abriendo la gráfica de f(h)... (Cierra la ventana para ver el análisis y la tabla)")
    
    # Evaluamos h desde -5 hasta 10 para ver el comportamiento cúbico completo
    h_vals = [i * 0.1 for i in range(-50, 101)] 
    y_vals = [f_py(h) for h in h_vals]
    
    plt.figure(figsize=(9, 5))
    plt.plot(h_vals, y_vals, label='$f(h) = \\pi h^2 \\frac{9-h}{3} - 30$', color='#16a085', linewidth=2.5)
    
    # Sombrear la zona física posible (0 <= h <= 6)
    plt.axvspan(0, 6, color='#3498db', alpha=0.15, label='Rango Físicamente Posible (0 a 2R)')
    
    plt.axhline(0, color='#e74c3c', linestyle='--', linewidth=1.5)
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    
    plt.title('Problema 05 - Posibles Respuestas (Raíces)', fontsize=14, pad=15)
    plt.xlabel('Profundidad h [m]')
    plt.ylabel('f(h)')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.show()

# =========================================================================
# 📊 LÓGICA PRINCIPAL: ORQUESTADOR Y TABLA PASO A PASO
# =========================================================================

def main():
    # 1. Mostrar la gráfica
    mostrar_grafica()

    # 2. Imprimir Comentario Técnico
    print("\n" + "=" * 70)
    print("📝 COMENTARIO DE LAS POSIBLES RESPUESTAS (Análisis Físico)")
    print("=" * 70)
    print("Como se observa en la gráfica, la ecuación cúbica tiene 3 raíces reales.")
    print("Sin embargo, al tratarse del diseño de un tanque esférico de radio R = 3 m:")
    print("  • La altura máxima del tanque (diámetro) es 6 m.")
    print("  • Por lo tanto, físicamente, la profundidad 'h' debe estar entre 0 y 6 m.")
    print("  • La raíz negativa carece de sentido (no hay alturas negativas).")
    print("  • La raíz mayor a 6 carece de sentido (el agua rebasaría el tanque).")
    print("Conclusión: Solo la raíz que se encuentra dentro del área sombreada")
    print("            es la solución de ingeniería correcta.\n")

    # 3. Cargar la librería C++
    try:
        lib = ctypes.CDLL('./libraices.so')
    except OSError:
        print("❌ Error: No se encontró 'libraices.so'.")
        return

    # 4. Configurar Interfaz de Newton-Raphson
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)
    c_f  = CMPFUNC(f_py)
    c_df = CMPFUNC(df_py)

    lib.newton_raphson.argtypes = [CMPFUNC, CMPFUNC, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.newton_raphson.restype = ctypes.c_double

    # 5. Ejecutar y generar tabla paso a paso
    print("=" * 55)
    print("⚙️  MÉTODO DE NEWTON-RAPHSON (Paso a paso)")
    print("=" * 55)
    print(f"{'Iteración':<10} | {'Profundidad h [m]':<20} | {'Ea (%)':<15}")
    print("-" * 55)

    p0 = 3.0 # Valor inicial dado por el problema (h = R)
    c_prev = p0
    tol_ea = 0.1
    max_iter_total = 25

    # Le pedimos al C++ que se detenga iteración por iteración
    for i in range(1, max_iter_total + 1):
        iter_ptr = ctypes.c_int(0)
        
        # Mandamos tol=0.0 para forzar a C++ a hacer exactamente 'i' iteraciones
        args = [c_f, c_df, ctypes.c_double(p0), ctypes.c_double(0.0), ctypes.c_double(100.0), ctypes.c_double(0.0), ctypes.c_int(i), ctypes.byref(iter_ptr)]
        h_actual = lib.newton_raphson(*args)
        
        # Calcular el Error Aproximado (Ea)
        if h_actual != 0:
            ea = absoluto((h_actual - c_prev) / h_actual) * 100.0
        else:
            ea = 0.0

        # Imprimir fila
        print(f"{i:<10} | {h_actual:<20.8f} | {ea:<15.6f}")

        # Condición de paro (Ea <= 0.1%)
        if ea <= tol_ea and i > 1:
            print("-" * 55)
            print(f"✅ CONVERGENCIA ALCANZADA: El tanque debe llenarse a {h_actual:.4f} m\n")
            break
            
        c_prev = h_actual

if __name__ == "__main__":
    main()