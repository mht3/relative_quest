import argparse
import typer
import os

def main():
    parser=argparse.ArgumentParser(
        prog = "relative_quest",
        description = "Command-line tool to perform relative finding using GERMLINE and ERSA"
    )

    parser.add_argument("mapfile", help=".map file", type=str)
    parser.add_argument("pedfile", help=".ped file", type=str)

    parser.add_argument("-o", "--out", help="Write output to file. " \
                                            "Default: stdout", metavar="FILE", type=str, required=False)

    args = parser.parse_args()

    if not os.path.isfile(args.mapfile):
        typer.echo("INVALID .map FILE PATH ")
        return

    if not os.path.isfile(args.pedfile):
        typer.echo("INVALID .ped FILE PATH ")
        return

    #TODO: CALL GERMLINE FUNCTION WITH THESE PARAMS
    typer.echo("SUCCESS! Output files have been created")


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
