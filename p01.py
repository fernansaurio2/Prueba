#Fernando José Padilla Cruz - PC24039
import ctypes

# Función auxiliar para valor absoluto sin importar 'math'
def absoluto(valor):
    return -valor if valor < 0 else valor

def main():
    print("Problema 01 - Resolución Híbrida (Python + C++)")
    print("================================================\n")

    # ---------------------------------------------------------
    # CASO 1: NEWTON - RAPHSON (Llamando a libraices.so)
    # ---------------------------------------------------------
    print("a) Raiz por newton_raphson (Calculado en C++):\n")
    
    # 1. Cargar librería compilada
    try:
        lib = ctypes.CDLL('./libraices.so')
    except OSError:
        print("❌ Error: No se encontro 'libraices.so'. Asegúrate de compilarla.")
        return

    # 2. Definir el prototipo de las funciones Callback (Python -> C++)
    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)

    # Funciones algebraicas puras (sin librerías matemáticas)
    def f_py(x):
        return (x * x) - 0.5

    def df_py(x):
        return 2.0 * x

    c_f = CMPFUNC(f_py)
    c_df = CMPFUNC(df_py)

    # 3. Configurar los argumentos exactos de la función en C++
    lib.newton_raphson.argtypes = [
        CMPFUNC, CMPFUNC, 
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, 
        ctypes.c_int, ctypes.POINTER(ctypes.c_int)
    ]
    lib.newton_raphson.restype = ctypes.c_double

    # 4. Parámetros del problema
    p0 = 3.00000000
    tol_ea = 0.1
    tol_et = 0.1
    valor_verdadero = 0.707106781187
    max_iter = 25
    iteraciones = ctypes.c_int(0)

    # 5. Ejecutar la librería
    raiz_nr = lib.newton_raphson(
        c_f, c_df, 
        ctypes.c_double(p0), 
        ctypes.c_double(tol_ea), 
        ctypes.c_double(tol_et), 
        ctypes.c_double(valor_verdadero), 
        ctypes.c_int(max_iter), 
        ctypes.byref(iteraciones)
    )

    print(f"\nEl valor de SQRT (0.500000) devuelto por la librería C++ es: {raiz_nr:.8f}\n")

    # ---------------------------------------------------------
    # CASO 2: SERIE DE TAYLOR (Ciclo repetitivo en Python)
    # ---------------------------------------------------------
    print("b) Iteración | Valor | Et | et")
    print("-" * 55)

    x_serie = -0.5
    T_old = 1.0
    suma_serie = 1.0
    
    ea = 100.0
    et = 100.0
    iteracion_serie = 1
    valor_anterior_serie = suma_serie

    # Ciclo repetitivo Mientras
    while (ea >= tol_ea or et >= tol_et) and iteracion_serie <= max_iter:
        # Relación de recurrencia
        numerador = 3.0 - 2.0 * iteracion_serie
        denominador = 2.0 * iteracion_serie
        T_new = T_old * (numerador / denominador) * x_serie

        suma_serie += T_new

        # Calcular errores
        et = absoluto((valor_verdadero - suma_serie) / valor_verdadero) * 100.0
        ea = absoluto((suma_serie - valor_anterior_serie) / suma_serie) * 100.0

        # Imprimir fila de la tabla
        print(f"   {iteracion_serie} | {suma_serie:.6f} | {et:.6f} | {ea:.6f}")

        T_old = T_new
        valor_anterior_serie = suma_serie
        iteracion_serie += 1

    print("-" * 55)
    print(f"El valor de SQRT (0.500000) por Serie es: {suma_serie:.6f}")

if __name__ == "__main__":
    main()