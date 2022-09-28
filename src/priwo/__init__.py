from rich.console import Console
from priwo._version import version
from rich.traceback import install

console = Console()
install(console=console)

__all__ = ["version"]
