from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver  # Cambiado de qiskit.algorithms
import numpy as np

def ejecutar_qubo(cultivo, latitud, longitud):
    """Versión actualizada para Qiskit moderno"""
    try:
        # 1. Crear problema de optimización
        qp = QuadraticProgram()
        qp.binary_var('x')
        qp.minimize(linear={'x': 1})
        
        # 2. Configurar solver
        solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
        
        # 3. Resolver
        result = solver.solve(qp)
        
        # 4. Retornar resultados (simulados para el ejemplo)
        return {
            'status': 'success',
            'configuracion': {'x': bool(result.x[0])},
            'rendimiento': 2500 + (result.fval * 100),  # Ejemplo
            'riesgo': 15 - (result.fval * 2),          # Ejemplo
            'recomendaciones': ['Configuración óptima calculada'],
            'rmse': 10.5,
            'roi': 15.8
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Error en QUBO: {str(e)}",
            'configuracion': None,
            'rendimiento': 0,
            'riesgo': 0,
            'recomendaciones': [],
            'rmse': 0,
            'roi': 0
        }