import click

from .main import main


@main.command()
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
def conv(
    infile: click.Path,
    outfile: click.Path,
):

    """
    Convert a pulsar data file from format into another.
    """

    pass