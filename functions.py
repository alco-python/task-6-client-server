import math
from typing import Any, Dict

def linear(x: float, params: Dict[str, Any]) -> float:
    # y = a * x + b
    a = params.get("a", 1.0)
    b = params.get("b", 0.0)
    return a * x + b

def quadratic(x: float, params: Dict[str, Any]) -> float:
    # y = a * x^2 + b * x + c
    a = params.get("a", 1.0)
    b = params.get("b", 0.0)
    c = params.get("c", 0.0)
    return a * x**2 + b * x + c

def sinusoidal(x: float, params: Dict[str, Any]) -> float:
    # y = a sin(w * x + p) + c
    a = params.get("a", 1.0)
    w = params.get("w", 1.0)
    phi = params.get("p", 0.0)
    offset = params.get("c", 0.0)
    return a * math.sin(w * x + phi) + offset

def exponential(x: float, params: Dict[str, Any]) -> float:
    # y = a * exp(k * x) + c
    a = params.get("a", 1.0)
    k = params.get("k", 0.1)
    c = params.get("c", 0.0)
    return a * math.exp(k * x) + c