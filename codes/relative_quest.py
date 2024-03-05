import argparse
import typer
import os

from .germline import GERMLINE
from .ersa import ERSA
def main():
    parser=argparse.ArgumentParser(
        prog = "relative_quest",
        description = "Command-line tool to perform relative finding using GERMLINE and ERSA"
    )

    parser.add_argument("mapfile", help=".map file", type=str)
    parser.add_argument("pedfile", help=".ped file", type=str)

    parser.add_argument("-o", "--out", help="Output prefix" \
                                            "Default: relative_quest", metavar="FILE", type=str)

    args = parser.parse_args()

    #CHECK VALID FILE PATHS
    if (not os.path.isfile(args.mapfile)) or (not args.mapfile.endswith('.map')):
        typer.echo("INVALID .map FILE/PATH")
        return

    if (not os.path.isfile(args.pedfile)) or (not args.pedfile.endswith('.ped')):
        typer.echo("INVALID .ped FILE/PATH")
        return

    if args.out is None:
        args.out = "relative_quest"

    #CALL GERMINE
    germline = GERMLINE(args.mapfile, args.pedfile, args.out)
    germline.perform_germline()

    #CALL ERSA
    ersa = ERSA(match_file=args.out + ".match", out=args.out)
    ersa.predict_ibd()
    typer.echo("SUCCESS! Output files have been created")


if __name__ == '__main__':
    main()
