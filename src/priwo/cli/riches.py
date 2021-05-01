from numpy import ndarray
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from typing import Dict, Callable
from rich.highlighter import RegexHighlighter


class DataHighlighter(RegexHighlighter):

    """"""

    base_style = "data."
    highlights = [
        r"(?P<colon>[:])",
        r"(?P<true>^True$)",
        r"(?P<false>^False$)",
        r"(?P<numeral>^[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?)$",
    ]


theme = Theme(
    {
        "data.colon": "bold magenta",
        "data.array": "bold white",
        "data.true": "bold green",
        "data.false": "bold red",
        "data.numeral": "bold yellow",
    }
)
console = Console(
    highlighter=DataHighlighter(),
    theme=theme,
)


def working(func: Callable):

    """"""

    def wrap(*args, **kwargs):
        with console.status("Working..."):
            func(*args, **kwargs)

    return wrap


@working
def pretty(
    title: str,
    content: Dict,
):

    """"""

    high = DataHighlighter()

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    for key, val in content.items():

        lcol = Text(key)
        lcol.stylize("bold")

        if isinstance(val, str):

            rcol = Text(val)
            rcol.stylize("italic")

        elif isinstance(val, (int, float)):

            rcol = high(str(val))

        elif isinstance(val, list):

            if len(val) > 0:
                rcol = Text("\n".join([str(_) for _ in val]))
                rcol.stylize("italic")
            else:
                rcol = Text("None")
                rcol.stylize("bold red")

        elif isinstance(val, ndarray):

            rcol = Text(
                "Array of size {:d} and dimensions {:s}".format(
                    val.size,
                    " x ".join(["{:d}".format(_) for _ in val.shape]),
                )
            )

        elif val is None:

            rcol = Text("None")
            rcol.stylize("bold red")

        else:

            rcol = Text(str(val))

        grid.add_row(lcol, rcol)

    console.print(
        Panel(
            grid,
            expand=False,
            title=title,
        )
    )