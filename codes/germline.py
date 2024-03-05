import numpy as np
from scipy import stats
import pandas as pd
import os
class GERMLINE:
    def __init__(self, mapfile, pedfile, out='relative_quest'):
        '''
        params
            mapfile: string
                path to the GERMLINE input .map file.
            pedfile: string
                path to the GERMLINE input .ped file.
            out: string
                output filename
        '''
        # segment length > 2.5 cM achieves false-negative
        # rate < 1% based upon germline.
        self.mapfile = mapfile
        self.pedfile = pedfile
        self.out = out

    def perform_germline(self):
        command = "germline -input " + self.pedfile + " " + self.mapfile + " -output " + self.out
        os.system(command)


if __name__ == '__main__':
    # germline outputs a .match file
    mapfile = '../data/test/germline/lwk_chr9.map'
    pedfile = '../data/test/germline/lwk_chr9.ped'
    germline = GERMLINE(mapfile, pedfile)
    # print(ersa.data)
    germline.out