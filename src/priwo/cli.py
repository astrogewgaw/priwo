import re
import click
import priwo
import numpy as np

from pathlib import Path
from typing import Any, Dict
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.highlighter import ReprHighlighter


console = Console()

name = lambda path: Path(path).name
suffix = lambda path: Path(path).suffix


def dims(arr: np.ndarray):

    """
    Get the dimensions of a `numpy.ndarray` as a nicely-formatted string.
    """

    return "Array of size {:d} and dimensions {:s}".format(
        arr.size,
        " x ".join(["{:d}".format(_) for _ in arr.shape]),
    )


def high(obj: Any):

    """
    Highlight a piece of text, except if it is a string.
    Uses `ReprHighlighter` from the `rich` module to do
    the actual highlighting. This ensures that numbers
    and data structures look nice.
    """

    reprh = ReprHighlighter()
    if isinstance(obj, str):
        return "[bold]{:s}[/bold]".format(obj)
    elif isinstance(obj, np.ndarray):
        return reprh(dims(obj))
    else:
        return reprh(str(obj))


def gridder(data: Dict):

    """
    Make a grid from a dictionary full of data.
    """

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    for key, val in data.items():
        grid.add_row(high(key), high(val))

    return grid


@click.group()
def cli():

    """
    The priwo command line tool.
    """

    pass


@cli.command()
@click.option(
    "--ext",
    type=str,
    default=None,
    required=False,
)
@click.argument(
    "infile",
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
def peek(ext, infile):

    """
    Peek into a pulsar data file.
    """

    with console.status("Reading..."):
        try:

            if ext is None:
                ext = suffix(infile)
            else:
                ext = "".join([".", ext])

            data = priwo.exts[ext](infile)

            panel = Panel(
                gridder(data),
                expand=False,
                title=name(infile),
            )
            console.print(panel)

        except KeyError:

            console.print(
                re.sub(
                    "\n+|\t+|\s{2,}",
                    " ",
                    """
                    Files of format [yellow]{:s}[/yellow] are [bold]not supported[/bold]
                    by priwo yet. Exiting...
                    """,
                )
            )


@cli.command()
@click.argument(
    "infile",
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
@click.argument(
    "outfile",
    type=click.Path(
        exists=False,
        writable=True,
        readable=False,
        file_okay=True,
        dir_okay=False,
        allow_dash=True,
        resolve_path=True,
    ),
)
def convert(infile, outfile):

    """
    Convert a pulsar data file from one format into another.
    """

    console.print("Input file path supplied: {:s}".format(infile))
    console.print("Output file path supplied: {:s}".format(outfile))
    console.print("[bold]Not yet implemented. Exiting...[/bold]")