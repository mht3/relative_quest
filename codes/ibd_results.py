import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def plot_ibd(ibd_df):
  fig, axes = plt.subplots(1, 3, figsize=(12, 4)) 
  # IBD=1 vs IBD=0
  axes[0].scatter(ibd_df["Z0"], ibd_df["Z1"], label="IBD=1 vs IBD=0")
  axes[0].set_xlabel("P(IBD=0)", size=10)
  axes[0].set_ylabel("P(IBD=1)", size=10)
  axes[0].legend()

  # IBD=2 vs IBD=1
  axes[1].scatter(ibd_df["Z1"], ibd_df["Z2"], label="IBD=2 vs IBD=1")
  axes[1].set_xlabel("P(IBD=1)", size=10)
  axes[1].set_ylabel("P(IBD=2)", size=10)
  axes[1].legend()

  # IBD=2 vs IBD=0
  axes[2].scatter(ibd_df["Z0"], ibd_df["Z2"], label="IBD=2 vs IBD=0")
  axes[2].set_xlabel("P(IBD=0)", size=10)
  axes[2].set_ylabel("P(IBD=2)", size=10)
  axes[2].legend()

  # Adjust layout
  fig.suptitle("Distribution of IBD Probabilities", fontsize=12)
  plt.tight_layout()
  plt.show()

if __name__ == '__main__':
    # example on how to plot a plink.genome output file
    filename = "data/test/plink/lwk.ibd.genome"
    ibd = pd.read_csv(filename, delim_whitespace=True)
    plot_ibd(ibd_df=ibd)

    # example how to run and plot ersa.genome output file