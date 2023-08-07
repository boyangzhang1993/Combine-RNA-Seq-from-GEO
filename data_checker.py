import tarfile
from pathlib import Path
import pandas as pd
from data_process import GE_FILE, TPM_ID
from utility import name_extract

RNA_FILE_PATH = Path('./RNA_Raw/GSE223695_RAW')
if __name__ == "__main__":
    df = pd.read_csv('Combined_RNA_TPM(from_Salmon).csv', index_col=0)
    row_names = df.index.tolist()
    # Iterating over columns
    for col in df.columns:
        print(f"Column Name: {col}")
        print("---------------")
        # Extracting entire data of column as list
        column_data = df[col].tolist()
        file_paths = list(RNA_FILE_PATH.glob('*.tar.gz'))
        matched_paths = [path for path in file_paths if col in path.name]
        if len(matched_paths) != 1:
            raise ValueError
        matching_path = matched_paths[0]

        # Create a temporary directory for extraction
        temp_dir = RNA_FILE_PATH.parent / 'decompressed'
        temp_dir.mkdir(exist_ok=True)

        # Extract the tar.gz file into the temporary directory
        with tarfile.open(matching_path, 'r:gz') as archive:
            archive.extractall(path=temp_dir)
        id_file, sample_name = name_extract(matching_path)
        # Now, read the "quant.sf" from the temporary directory
        quant_path = temp_dir / id_file / GE_FILE

        if quant_path.exists() and sample_name:
            # Read the TPM column from the quant.sf file
            df_original = pd.read_csv(quant_path, sep='\t', usecols=['Name', TPM_ID])
            # Add to dictionary
            data_match = df_original.set_index('Name')[TPM_ID].tolist() == column_data
            # Save the gene names in the all_gene_names dictionary
            gene_match = df_original['Name'].tolist() == row_names
            if not data_match or not gene_match:
                raise ValueError
            print("Passed")
    print("All passed")
