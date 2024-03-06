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

    parser.add_argument("inputdir", help="Directory with all input .map and .ped files", type=str)

    parser.add_argument("-o", "--out", help="Output prefix" \
                                            "Default: relative_quest", metavar="FILE", type=str)

    args = parser.parse_args()

    #CHECK VALID DIRECTORY
    if not os.path.exists(args.inputdir):
        typer.echo("INVALID PATH")
        return


    allfiles = os.listdir(args.inputdir)
    mapfiles = [f for f in allfiles if f.endswith('.map')]
    pedfiles = [f for f in allfiles if f.endswith('.ped')]

    if(len(mapfiles) != len(pedfiles)):
        typer.echo("ERROR! Not equal number of .map and .ped files in input directory")
        return

    if args.out is None:
        args.out = "relative_quest"

    try:
        #CALL GERMLINE FOR EACH PAIR OF INPUT FILES:
        for mf in mapfiles:
            prefix = mf[:len(mf)-4]
            pf = prefix + '.map'
            pf_path = args.inputdir + '\\' + pf
            if not os.path.isfile(pf_path):
                typer.echo("ERROR!! NO MATCHING .ped FILE FOR .map FILE. PLEASE CHECK INPUT FILES")
                return
            #CALL GERMLINE
            outputfilesprefix = args.inputdir + "\\" + prefix + "_germline"
            mf_path = args.inputdir + "\\" + mf
            pf_path = args.inputdir + "\\" + pf
            germline = GERMLINE(mf_path, pf_path, outputfilesprefix)
            ret = germline.perform_germline()
            typer.echo(ret)
    except:
        typer.echo("ERROR IN GERMLINE!!")
        return


    #CONCATENATE .match FILES
    allfiles = os.listdir(args.inputdir)
    matchfiles = [f for f in allfiles if f.endswith('.match')]
    finalmatchfile = args.inputdir + "\\expected.match"
    with open(finalmatchfile, 'w') as outfile:
        for fname in matchfiles:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


    #CALL ERSA
    ersa = ERSA(match_file=finalmatchfile, out=args.out)
    ersa.predict_ibd()
    typer.echo("SUCCESS! Output files have been created")


if __name__ == '__main__':
    main()
