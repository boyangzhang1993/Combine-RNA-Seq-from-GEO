import shutil
from pathlib import Path
import pandas as pd
import tarfile
from utility import name_match, check_genes_name_consistent, download_and_decompress

# Constant (see Assumptions for description)
DOWNLOAD_URL = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE223695&format=file"  # Download URL
RNA_FILE_PATH = Path('./RNA_Raw/GSE223695_RAW')

PATTERN = r'_quant\.tar$'
GE_FILE ='quant.sf'
GE_SPILT = '\t'
TPM_ID = 'TPM'
RE_CHECK = True

'''
Inputs:
1. Download url
2. File saving path 

Assumptions:
1. "GSM" is used as a prefix of the sample name. 
2. Additional experiment identifiers are following the "GSM" such as "B9053" and "WT-HSC-TET2-HM-DIR"
3. "TPM" is the gene expression data which is recorded in 'quant.sf'

Auto checks (derisk):
1. Check for gene names are consistent across files
2. After generating combined data, check numbers are matching with the original files. 


Output:
Combined_RNA_TPM(from_Salmon).csv
1. genes (rows) by samples (columns) containing the RNA-Seq read counts (TPM)
2. Please note the RNA data were already processed using Salmon as stated in https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223695
'''

if __name__ == "__main__":
    # Download if missing file
    download_and_decompress(RNA_FILE_PATH, DOWNLOAD_URL)
    # Create a dictionary to store data: {filename: data}
    data_dict = {}
    # List to store gene names from each file
    all_gene_names = {}

    for gz_file in RNA_FILE_PATH.glob('*.tar.gz'):
        if gz_file.name.startswith("._"):
            continue
        # Create a temporary directory for extraction
        temp_dir = RNA_FILE_PATH.parent / 'decompressed'
        temp_dir.mkdir(exist_ok=True)

        # Extract the tar.gz file into the temporary directory
        with tarfile.open(gz_file, 'r:gz') as archive:
            archive.extractall(path=temp_dir)
        id_file, sample_name = name_match(gz_file)
        # Now, read the "quant.sf" from the temporary directory
        quant_path = temp_dir / id_file / GE_FILE

        if quant_path.exists() and sample_name:
            # Read the TPM column from the quant.sf file
            df = pd.read_csv(quant_path, sep=GE_SPILT, usecols=['Name', TPM_ID])
            # Add to dictionary
            data_dict[sample_name] = df.set_index('Name')[TPM_ID]
            # Save the gene names in the all_gene_names dictionary
            all_gene_names[sample_name] = df['Name']


    # Check for gene name consistency across files
    consistent = check_genes_name_consistent(all_gene_names)
    # Convert dictionary to DataFrame if consistent
    if not consistent:
        raise ValueError

    combined_df = pd.DataFrame(data_dict)
    print(combined_df)
    # Remove temporary directory after processing
    shutil.rmtree(temp_dir)
    # Convert dictionary to DataFrame
    combined_df.to_csv('Combined_RNA_TPM(from_Salmon).csv', index=True)





