"""
Core Bisection Method Algorithm Module
Separated from GUI for better code organization and reusability.
"""

import math
from typing import Callable, Dict, List, Union, Optional


def target_function(x: float) -> float:
    """
    Target function: f(x) = x^3 - x^2 - 4x
    This function has three roots:
    - x1: negative root between -2 and -1
    - x2: root at x = 0
    - x3: positive root between 2 and 3
    """
    return x**3 - x**2 - 4*x


def general_function_evaluator(x: float, function_str: str) -> float:
    """
    Safely evaluate a mathematical function string at point x.
    
    Args:
        x: Point to evaluate the function at
        function_str: String representation of the function
        
    Returns:
        Function value at x
        
    Raises:
        ValueError: If function expression is invalid
    """
    try:
        # Replace common mathematical notation
        function_str = function_str.replace('^', '**')
        function_str = function_str.replace('sin', 'math.sin')
        function_str = function_str.replace('cos', 'math.cos')
        function_str = function_str.replace('tan', 'math.tan')
        function_str = function_str.replace('log', 'math.log')
        function_str = function_str.replace('exp', 'math.exp')
        function_str = function_str.replace('sqrt', 'math.sqrt')
        function_str = function_str.replace('abs', 'abs')
        
        # Create a safe namespace for evaluation
        namespace = {'x': x, 'math': math, 'e': math.e, 'pi': math.pi}
        return eval(function_str, {"__builtins__": {}}, namespace)
    except Exception as e:
        raise ValueError(f"Invalid function expression: {str(e)}")


def bisection_method(
    func: Union[Callable[[float], float], str],
    a: float,
    b: float,
    tolerance: float = 1e-6,
    max_iterations: int = 100
) -> Dict:
    """
    Find root using bisection method.
    
    Args:
        func: Function to find root for (callable or string expression)
        a: Left endpoint of initial interval
        b: Right endpoint of initial interval
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations
        
    Returns:
        Dictionary containing:
        - 'root': Found root value
        - 'function_value': Function value at root
        - 'iterations': Number of iterations performed
        - 'converged': Whether method converged
        - 'error': Final error estimate
        - 'iteration_data': List of iteration details
    """
    
    # Handle function input
    if isinstance(func, str):
        def f(x):
            return general_function_evaluator(x, func)
    else:
        f = func
    
    # Validate initial interval
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        raise ValueError(
            f"Root is not bracketed in interval [{a}, {b}]. "
            f"f({a}) = {fa:.6f}, f({b}) = {fb:.6f}. "
            "f(a) and f(b) must have opposite signs."
        )
    
    iteration_data = []
    iteration = 0
    
    while iteration < max_iterations:
        # Calculate midpoint
        c = (a + b) / 2
        fc = f(c)
        error = (b - a) / 2
        
        # Store iteration data
        iteration_data.append({
            'iteration': iteration + 1,
            'a': a,
            'b': b,
            'c': c,
            'f_a': f(a),
            'f_b': f(b),
            'f_c': fc,
            'error': error,
            'interval_width': b - a
        })
        
        # Check convergence
        if abs(fc) < tolerance or error < tolerance:
            return {
                'root': c,
                'function_value': fc,
                'iterations': iteration + 1,
                'converged': True,
                'error': error,
                'iteration_data': iteration_data
            }
        
        # Update interval
        if f(a) * fc < 0:
            b = c
        else:
            a = c
            
        iteration += 1
    
    # Maximum iterations reached
    c = (a + b) / 2
    fc = f(c)
    error = (b - a) / 2
    
    return {
        'root': c,
        'function_value': fc,
        'iterations': max_iterations,
        'converged': False,
        'error': error,
        'iteration_data': iteration_data
    }


def find_all_roots_target_function() -> List[Dict]:
    """
    Find all three roots of the target function f(x) = x^3 - x^2 - 4x.
    Uses predefined intervals based on function analysis.
    
    Returns:
        List of dictionaries, each containing root finding results
    """
    
    # Define intervals for each root based on function analysis
    intervals = [
        {'name': 'x1 (negative root)', 'a': -2.0, 'b': -1.0},
        {'name': 'x2 (zero root)', 'a': -0.5, 'b': 0.5},
        {'name': 'x3 (positive root)', 'a': 2.0, 'b': 3.0}
    ]
    
    results = []
    
    for interval in intervals:
        try:
            result = bisection_method(
                target_function,
                interval['a'],
                interval['b'],
                tolerance=1e-10,
                max_iterations=100
            )
            result['root_name'] = interval['name']
            result['initial_interval'] = [interval['a'], interval['b']]
            results.append(result)
        except ValueError as e:
            results.append({
                'root_name': interval['name'],
                'initial_interval': [interval['a'], interval['b']],
                'error_message': str(e),
                'converged': False
            })
    
    return results


def format_iteration_table(iteration_data: List[Dict]) -> str:
    """
    Format iteration data as a readable table string.
    
    Args:
        iteration_data: List of iteration dictionaries
        
    Returns:
        Formatted table string
    """
    if not iteration_data:
        return "No iteration data available."
    
    # Header
    header = f"{'Iter':<4} {'a':<12} {'b':<12} {'c':<12} {'f(c)':<12} {'Error':<12} {'Width':<12}"
    separator = "-" * len(header)
    
    lines = [header, separator]
    
    # Data rows
    for data in iteration_data:
        line = (
            f"{data['iteration']:<4} "
            f"{data['a']:<12.6f} "
            f"{data['b']:<12.6f} "
            f"{data['c']:<12.6f} "
            f"{data['f_c']:<12.6e} "
            f"{data['error']:<12.6e} "
            f"{data['interval_width']:<12.6e}"
        )
        lines.append(line)
    
    return '\n'.join(lines)


def format_results(result: Dict) -> str:
    """
    Format bisection method results as a readable string.
    
    Args:
        result: Result dictionary from bisection_method
        
    Returns:
        Formatted result string
    """
    if not result.get('converged', False):
        return f"""
Results:
========
Status: Did not converge
Approximate root: {result.get('root', 'N/A'):.10f}
Function value: {result.get('function_value', 'N/A'):.2e}
Iterations: {result.get('iterations', 'N/A')}
Final error: {result.get('error', 'N/A'):.2e}
"""
    
    return f"""
Results:
========
Status: Converged successfully
Root: {result['root']:.10f}
Function value: {result['function_value']:.2e}
Iterations: {result['iterations']}
Final error: {result['error']:.2e}
"""


if __name__ == "__main__":
    # Test the module
    print("Testing Bisection Method Core Module")
    print("=" * 50)
    
    # Test target function
    print(f"Target function: f(x) = x^3 - x^2 - 4x")
    print(f"f(-2) = {target_function(-2)}")
    print(f"f(-1) = {target_function(-1)}")
    print(f"f(0) = {target_function(0)}")
    print(f"f(2) = {target_function(2)}")
    print(f"f(3) = {target_function(3)}")
    print()
    
    # Find all roots
    print("Finding all roots:")
    roots = find_all_roots_target_function()
    
    for i, result in enumerate(roots, 1):
        print(f"\nRoot {i}: {result.get('root_name', 'Unknown')}")
        if result.get('converged', False):
            print(f"Value: {result['root']:.10f}")
            print(f"Iterations: {result['iterations']}")
        else:
            print(f"Failed to converge: {result.get('error_message', 'Unknown error')}")