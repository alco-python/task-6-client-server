import uvicorn
from fastapi import FastAPI, HTTPException
from manager import FunctionManager
import functions

app = FastAPI(title="Parametric Function Server")

manager = FunctionManager()

BUILTIN_SPECS = {
    "linear": (functions.linear, {"a": 1.0, "b": 0.0}),
    "quadratic": (functions.quadratic, {"a": 1.0, "b": 0.0, "c": 0.0}),
    "sinusoidal": (functions.sinusoidal, {"a": 1.0, "w": 1.0, "p": 0.0, "c": 0.0}),
    "exponential": (functions.exponential, {"a": 1.0, "k": 0.1, "c": 0.0}),
}

for name, (func, params) in BUILTIN_SPECS.items():
    manager.register_builtin(name, func, params)

manager.load_all()


@app.get("/functions")
async def list_functions():
    return {"functions": manager.list_names()}


@app.get("/functions/{name}")
async def get_function(name: str):
    try:
        return manager.get_metadata(name)
    except KeyError:
        raise HTTPException(404, f"Function '{name}' not found")


@app.put("/functions/{name}")
async def update_function(name: str, parameters: dict):
    if name not in BUILTIN_SPECS:
        raise HTTPException(400, f"Unknown function '{name}'")
    try:
        manager.update(name, new_parameters=parameters)
        return manager.get_metadata(name)
    except KeyError:
        raise HTTPException(404, f"Function '{name}' not found")
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/functions/{name}/call")
async def call_function(name: str, payload: dict):
    x = payload.get("x")
    if x is None:
        raise HTTPException(400, "'x' is required")
    try:
        result = manager.call(name, x)
        return {"result": result}
    except KeyError:
        raise HTTPException(404, f"Function '{name}' not found")
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/functions/{name}")
async def delete_function(name: str):
    if manager.delete(name):
        return {"status": "success"}
    else:
        raise HTTPException(404, f"Function '{name}' not found")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)