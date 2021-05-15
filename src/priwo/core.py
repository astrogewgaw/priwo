from rich import print
from rich.table import Table
from rich.panel import Panel


MB = 1024 * 1024
GB = 1024 * 1024 * 1024

# The maximum chunk size that is used by priwo to read in data.
# Any data with a greater size than this will be read in chunks.
PRIWO_MAX_SIZE = 0.5 * GB


# The pulsar data formats supported by priwo. This list of dictionaries
# stores the name, the commonly-used extension for the files (if any),
# and a short description When adding new formats, contributers should
# remember to edit this dictionary as well. Only formats that are fully
# supported by priwo should be entered into this list.
PRIWO_AVAILABLE_FORMATS = [
    {"name": "inf", "ext": ".inf", "descr": "PRESTO metadata."},
    {"name": "sigproc", "ext": None, "descr": "SIGPROC metadata."},
    {"name": "dat", "ext": ".dat", "descr": "PRESTO time series data."},
    {"name": "tim", "ext": ".tim", "descr": "SIGPROC time series data."},
    {"name": "fft", "ext": ".fft", "descr": "PRESTO power/frequency spectrum data."},
    {"name": "spc", "ext": ".spc", "descr": "SIGPROC power/frequency spectrum data."},
    {"name": "pfd", "ext": ".pfd", "descr": "PRESTO folded data."},
    {"name": "polycos", "ext": ".polycos", "descr": "Polynomial coefficients."},
    {"name": "bestprof", "ext": ".bestprof", "descr": "PRESTO best profile data."},
]


def max_size():

    """
    Pretty print the maximum size set for reading/writing in priwo.
    """

    grid = Table.grid(padding=5)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    grid.add_row("Maximum size:", f"{PRIWO_MAX_SIZE / GB} GB")

    print(Panel(grid, expand=False))


def available_formats():

    """
    Pretty print the formats available for reading/writing in priwo.
    """

    table = Table(
        "Format name",
        "Common extension (if any)",
        "Description",
        title="Formats available in [bold]priwo[/bold].",
        expand=True,
    )

    for available in PRIWO_AVAILABLE_FORMATS:
        table.add_row(*available.values())

    print(table)


def chunks():

    """
    Read in binary data in chunks.
    """

    pass