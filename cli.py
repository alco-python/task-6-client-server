import json
import click
from manager import FunctionManager
import functions

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


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
@click.option("--params", "-p", default="{}", help='Parameters as JSON string, e.g. \'{"a":2, "b":5}\'')
def create(name: str, params: str):
    if name not in BUILTIN_SPECS:
        click.echo(f"Error: unknown function '{name}'. Available: {', '.join(BUILTIN_SPECS)}")
        return
    try:
        param_dict = json.loads(params)
        manager.create(name, BUILTIN_SPECS[name][0], param_dict)
        click.echo(f"Function '{name}' created and saved.")
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument("name")
@click.argument("x_str")
def call(name: str, x_str: str):
    try:
        x_val = eval(x_str, {"__builtins__": {}}, {})
        if not isinstance(x_val, (int, float, complex)):
            raise ValueError("x must be a number")
        result = manager.call(name, x_val)
        click.echo(f"{name}({x_str}) = {result}")
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command("list")
def list_funcs():
    names = manager.list_names()
    if names:
        click.echo("Functions:")
        for n in names:
            click.echo(f"  - {n}")
    else:
        click.echo("No functions.")


@cli.command()
@click.argument("name", required=False)
def info(name: str = None):
    try:
        if name:
            meta = manager.get_metadata(name)
            click.echo(f"\nFunction: {meta['name']}")
            click.echo(f"  Input:  {meta['input_signature']}")
            click.echo(f"  Output: {meta['output_signature']}")
            click.echo(f"  Params: {meta['parameters']}\n")
        else:
            for n in manager.list_names():
                meta = manager.get_metadata(n)
                click.echo(f"{n}: {meta['parameters']}")
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument("name")
def delete(name: str):
    if manager.delete(name):
        click.echo(f"Function '{name}' deleted.")
    else:
        click.echo(f"Function '{name}' not found.")


if __name__ == "__main__":
    cli()