import click
import priwo
import pathlib

from .main import main
from .riches import pretty


@main.command()
@click.option(
    "-e",
    "--ext",
    type=str,
    default="",
    required=False,
)
@click.argument(
    "fname",
    type=click.Path(
        exists=True,
        readable=True,
        writable=False,
        file_okay=True,
        dir_okay=False,
        allow_dash=True,
        resolve_path=True,
    ),
)
def peek(
    ext: str,
    fname: str,
):

    """
    Take a peek into any pulsar data file.
    """

    try:
        if ext == "":
            ext = pathlib.Path(fname).suffix
        else:
            ext = "".join([".", ext])
        pretty(
            title=pathlib.Path(fname).name,
            content=priwo.exts[ext](fname),
        )
    except KeyError:
        pass