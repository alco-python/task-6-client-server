import inspect
import json
import os
from typing import Any, Dict, Callable, List, Optional

STORAGE_DIR = "storage/functions"
os.makedirs(STORAGE_DIR, exist_ok=True)

class Function:
    def __init__(self, name: str, func: Callable, parameters: Dict[str, Any] = None):
        self.name = name
        self.func = func
        self.parameters = parameters or {}
        sig = inspect.signature(func)
        self.input_signature = str(sig)
        self.output_signature = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else "Any"

    def evaluate(self, x: Any) -> Any:
        return self.func(x, self.parameters)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "input_signature": self.input_signature,
            "output_signature": self.output_signature,
            "parameters": self.parameters.copy()
        }

    def save(self):
        path = os.path.join(STORAGE_DIR, f"{self.name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.parameters, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, name: str, func: Callable) -> Optional["Function"]:
        path = os.path.join(STORAGE_DIR, f"{name}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                params = json.load(f)
            return cls(name, func, params)
        except Exception:
            return None


class FunctionManager:
    def __init__(self):
        self.functions: Dict[str, Function] = {}
        self._builtin_funcs = {}

    def register_builtin(self, name: str, func: Callable, default_params: Dict[str, Any]):
        self._builtin_funcs[name] = (func, default_params)

    def load_all(self):
        for name, (func, default_params) in self._builtin_funcs.items():
            loaded = Function.load(name, func)
            if loaded:
                self.functions[name] = loaded
            else:
                self.functions[name] = Function(name, func, default_params.copy())

    def create(self, name: str, func: Callable, parameters: Dict[str, Any] = None) -> Function:
        if name in self.functions:
            raise ValueError(f"Function '{name}' already exists")
        f = Function(name, func, parameters)
        f.save()
        self.functions[name] = f
        return f

    def read(self, name: str) -> Function:
        if name not in self.functions:
            raise KeyError(f"Function '{name}' not found")
        return self.functions[name]

    def update(self, name: str, new_func: Optional[Callable] = None, new_parameters: Optional[Dict[str, Any]] = None) -> Function:
        func = self.read(name)
        if new_func is not None:
            func.func = new_func
            sig = inspect.signature(new_func)
            func.input_signature = str(sig)
            func.output_signature = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else "Any"
        if new_parameters is not None:
            func.parameters.update(new_parameters)
        func.save()
        return func

    def delete(self, name: str) -> bool:
        if name in self.functions:
            path = os.path.join(STORAGE_DIR, f"{name}.json")
            if os.path.exists(path):
                os.remove(path)
            del self.functions[name]
            return True
        return False

    def list_names(self) -> List[str]:
        return list(self.functions.keys())

    def call(self, name: str, x: Any) -> Any:
        return self.read(name).evaluate(x)

    def get_metadata(self, name: str) -> dict:
        return self.read(name).to_dict()