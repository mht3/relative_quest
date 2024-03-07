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

def predict_plink_results(ibd):
  relationships = {}
  lax_threshold = 0.1
  threshold = 0.05
  for i, row in ibd.iterrows():
      z0 = row['Z0']
      z1 = row['Z1']
      z2 = row['Z2']
      fid1 = row['FID1']
      fid2 = row['FID2']
      # parent child relationships
      if (z1 > 1. - lax_threshold):
        if relationships.get('Parent-child', -1) == -1:
          relationships['Parent-child'] = []
        relationships['Parent-child'].append([fid1, fid2])
      elif (z2 > 0.25 - threshold and z1 > 0.5 - lax_threshold):
        # siblings requirement
        if relationships.get('Siblings', -1) == -1:
          relationships['Siblings'] = []
        relationships['Siblings'].append([fid1, fid2])
      elif (z2 > 1. - lax_threshold):
        # Identical twins requirement
        if relationships.get('Identical Twins', -1) == -1:
          relationships['Identical Twins'] = []
        relationships['Identical Twins'].append([fid1, fid2])
      elif (z1 > 0.5 - 1.5*lax_threshold and z0 > 0.5 - 1.5*lax_threshold):
        if relationships.get('Second Order', -1) == -1:
          relationships['Second Order'] = []
        relationships['Second Order'].append([fid1, fid2])
      elif (z1 > 0.25 - lax_threshold and z0 > 0.75 - lax_threshold):
        if relationships.get('First Cousins', -1) == -1:
          relationships['First Cousins'] = []
        relationships['First Cousins'].append([fid1, fid2])
      elif (z1 > 0.0625):
        if relationships.get('Second Cousins', -1) == -1:
          relationships['Second Cousins'] = []
        relationships['Second Cousins'].append([fid1, fid2])
      elif (z1 > 1 / (2**6)):
        if relationships.get('Third Cousins', -1) == -1:
          relationships['Third Cousins'] = []
        relationships['Third Cousins'].append([fid1, fid2])
  return relationships

if __name__ == '__main__':
    # example on how to plot a plink.genome output file
    filename = "data/test/plink/lwk.ibd.genome"
    print('##### Plink #####')
    ibd = pd.read_csv(filename, sep='\s+')
    relationships = predict_plink_results(ibd)
    print({k:len(v) for k, v in relationships.items()})
    plot_ibd(ibd_df=ibd)

    # example how to run and plot ersa.genome output file