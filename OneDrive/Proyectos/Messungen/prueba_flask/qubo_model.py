from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import NumPyMinimumEigensolver
import numpy as np

def ejecutar_qubo(cultivo, latitud, longitud):
    """Función QUBO simplificada para pruebas"""
    try:
        # Problema de ejemplo mínimo
        qp = QuadraticProgram()
        qp.binary_var('x')
        qp.minimize(linear={'x': 1})
        
        solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
        result = solver.solve(qp)
        
        return {
            'status': 'success',
            'configuracion': {'x': bool(result.x[0])},
            'rendimiento': 2500,
            'riesgo': 15,
            'recomendaciones': ['Árboles de sombra recomendados'],
            'rmse': 12.5,
            'roi': 18.3
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }