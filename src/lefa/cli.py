import typer

from lefa.alpaca import ReadOnlyAlpaca
from lefa.config import Settings

app = typer.Typer(help="LEFA AI governed paper-trading interface")


@app.command()
def account() -> None:
    """Read and print normalized Alpaca paper-account telemetry."""
    state = ReadOnlyAlpaca(Settings()).account_state()
    typer.echo(state.model_dump_json(indent=2))
