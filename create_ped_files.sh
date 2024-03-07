#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_genotype_data_file> <output_directory_prefix>"
    exit 1
fi

input_prefix=$1
output_prefix=$2

# Determine file type
if [[ "$input_prefix" == *"vcf"* ]]; then
    file_type_flag="--vcf"
else
    file_type_flag="--bfile"
fi

# Iterate through chromosomes 1 to 22
for ((chr=1; chr<=22; chr++)); do
    echo "Processing chromosome $chr..."
    plink "${file_type_flag}" "${input_prefix}" --chr "$chr" --recode 12 --out "${output_prefix}_chr${chr}"
done

echo "Done!"
