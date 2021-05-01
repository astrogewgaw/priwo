import click


@click.group()
def main():

    """
    The priwo command line tool.

    This allows the user to access a part of priwo's functionality via
    the command line. It houses two sub-commands:

        peek:

            This allows the user to take a peek into any pulsar data file
            whose format is supported by `priwo`. The data is printed to
            the terminal with full ANSI color highlighting, thanks to the
            `rich` module.

        conv:

            This allows the user to convert pulsar data from a particular
            format into another (provided `priwo` supports said conversion).
            These conversions can also be achieved programatically (check
            out the documentation for some examples).
    """

    pass