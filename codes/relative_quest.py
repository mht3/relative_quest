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
