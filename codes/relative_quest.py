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

    parser.add_argument("-thresh", "--thresh", help="ERSA Threshold Value", type=float)
    parser.add_argument("-theta", "--theta", help="ERSA Theta Value", type=float)
    parser.add_argument("-d", "--d", help="Maximum d (combined number of generations separating " 
                                        "individuals from their ancestors)", type=int)
    parser.add_argument("-a", "--alpha", help="ERSA Alpha Value", type=float)


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

    typer.echo("Running GERMLINE on input files...")
    try:
        #CALL GERMLINE FOR EACH PAIR OF INPUT FILES:
        for mf in mapfiles:
            prefix = mf[:len(mf)-4]
            pf = prefix + '.ped'
            pf_path = os.path.join(args.inputdir,pf)
            if not os.path.isfile(pf_path):
                typer.echo("ERROR!! NO MATCHING .ped FILE FOR .map FILE. PLEASE CHECK INPUT FILES")
                return
            #CALL GERMLINE
            outputfilesprefix = os.path.join(args.inputdir,prefix + "_germline")
            mf_path = os.path.join(args.inputdir,mf)
            pf_path = os.path.join(args.inputdir,pf)
            germline = GERMLINE(mf_path, pf_path, outputfilesprefix)
            ret = germline.perform_germline()
            #typer.echo(ret)
    except Exception as ex:
        typer.echo("ERROR IN GERMLINE!!")
        typer.echo(ex)
        return

    typer.echo("GERMLINE FINISHED")
    typer.echo("ERSA STARTING...")
    #CONCATENATE .match FILES
    allfiles = os.listdir(args.inputdir)
    matchfiles = [os.path.join(args.inputdir,f) for f in allfiles if f.endswith('.match')]
    finalmatchfile = os.path.join(args.inputdir,"expected.match")
    with open(finalmatchfile, 'w') as outfile:
        for fname in matchfiles:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


    #CALL ERSA
    threshold = 2.5
    theta = 3.12
    max_d = 10
    alpha = 0.1

    if args.thresh is not None:
        threshold = args.thresh
    if args.theta is not None:
        theta = args.theta
    if args.d is not None:
        max_d = args.d
    if args.alpha is not None:
        alpha = args.alpha

    ersa = ERSA(match_file=finalmatchfile, threshold=threshold,
                 theta=theta, max_d=max_d, alpha=alpha, out=args.out)
    ersa.predict_ibd()
    #print(ersa.lambda_val)
    typer.echo("SUCCESS!")


if __name__ == '__main__':
    main()
