import click
import priwo
import pathlib

from .riches import pretty


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=priwo.__version__)
def main():

    """
    The priwo command line tool.
    """

    pass


@main.command()
def max():

    """
    Show the maximum size set in priwo.
    """

    priwo.max_size()


@main.command()
def available():

    """
    Show the available formats in priwo.
    """

    priwo.available_formats()


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
            contents=priwo.PRIWO_EXTS[ext](fname),
        )
    except KeyError:
        pass