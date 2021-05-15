from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.console import Console

from numpy import ndarray
from typing import (
    List,
    Dict,
    Tuple,
    Union,
    Callable,
)


console = Console()


NULL_TEXT = Text.from_markup("[bold bright_red]None")


def str_highlighter(txt: str) -> Text:

    """"""

    if txt:
        return Text.from_markup(f"[italic]{txt}")
    else:
        return NULL_TEXT


def num_highlighter(val: Union[int, float]) -> Text:

    """"""

    return Text.from_markup(f"[bold orange_red1]{str(val)}")


def bool_highlighter(val: bool) -> Text:

    """"""

    if val:
        return Text.from_markup("[bold bright_green]True")
    else:
        return Text.from_markup("[bold bright_red]False")


def list_highlighter(arr: List) -> Text:

    """"""

    if arr:
        if len(arr) == 1:
            arr_str = str(arr[0])
        else:
            arr_str = "\n".join([str(i) for i in arr])
        return Text.from_markup(f"[italic]{arr_str}")
    else:
        return NULL_TEXT


def numpy_highlighter(arr: ndarray) -> Text:

    """"""

    size = arr.size
    dims = " x ".join([str(dim) for dim in arr.shape])
    return Text.from_markup(
        f"Array of size [bold]{size}[/bold] and dimensions [bold]{dims}[/bold]"
    )


highlighters: Dict[Union[type, Tuple[type, type]], Callable] = {
    str: str_highlighter,
    list: list_highlighter,
    ndarray: numpy_highlighter,
    (int, float): num_highlighter,
}


def make_grid(content: Dict) -> Table:

    """"""

    grid = Table.grid(expand=False)

    grid.add_column()
    grid.add_column(justify="right")

    for key, val in content.items():

        left_col = f"[bold]{key}"

        for (
            val_type,
            val_highlighter,
        ) in highlighters.items():
            if isinstance(val, val_type) and not isinstance(val, bool):
                right_col = val_highlighter(val)

        if isinstance(val, bool):
            right_col = bool_highlighter(val)

        grid.add_row(left_col, right_col)

    return grid


def pretty(
    title: str,
    contents: Union[List, Dict],
) -> None:

    """"""

    if isinstance(contents, dict):
        display = Panel(make_grid(contents), expand=False, title=title)
    elif isinstance(contents, list):
        display = Panel(
            Columns(
                [
                    Panel(
                        make_grid(content),
                        expand=False,
                        title=str(ix + 1),
                    )
                    for ix, content in enumerate(contents)
                ],
                expand=True,
                align="center",
            ),
            title=title,
        )

    console.print(display)
