import argparse
import typer
def main():
    parser=argparse.ArgumentParser(
        prog = "rquest",
        description = "Command-line tool to perform relative finding using GERMLINE and ESRA"
    )

    parser.add_argument("matchf", help="Match file", type=str)

    args = parser.parse_args()
    typer.echo(args.matchf)


if __name__ == '__main__':
    main()
'''
from typing import Optional, List

import typer

from __init__ import __app_name__, __version__
from codes import ersa
app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

@app.command()
def findrelatives(
        matchfile: List[str] = typer.Argument(...),
        threshold: int = typer.Option(2, "--threshold", "-t", min=1, max=3),
) -> None:
    match_file = 'data/test/germline/expected.match'
    e = ersa.ERSA(match_file, threshold=2.5)
    typer.secho('SUCCESS! Generated file:')
'''
