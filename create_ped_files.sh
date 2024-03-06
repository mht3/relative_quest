#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_prefix> <output_prefix>"
    exit 1
fi

input_prefix=$1
output_prefix=$2

# Iterate through chromosomes 1 to 22
for ((chr=1; chr<=22; chr++)); do
    echo "Processing chromosome $chr..."
    plink --bfile "${input_prefix}" --chr "$chr" --recode 12 --out "${output_prefix}_chr${chr}"
done

echo "Done!"
