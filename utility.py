import pathlib
import re
import tarfile
from pathlib import Path

import requests


def name_match(gz_file: Path) -> (str, str):
    id_match = re.search(r'([^_]+)_quant\.tar$', gz_file.stem)
    sample_match = re.search(r"(GSM\d+)", gz_file.stem)
    if id_match:
        id_file = id_match.group(1)
        print(id_file)
        id_file += '_quant'
    if sample_match:
        sample_name = sample_match.group(1)

    return id_file, sample_name


def check_genes_name_consistent(all_gene_names: dict) -> bool:
    reference_genes = next(iter(all_gene_names.values()))  # Using the first set of genes as reference
    # Print the files which are inconsistent
    for filename, genes in all_gene_names.items():
        for gene, ref_gen in zip(genes, reference_genes):
            if gene != ref_gen:
                print("Warning: Some files have inconsistent gene names!")
                print(gene, ref_gen)
                return False

    print("All files have consistent gene names.")
    return True


def download_and_decompress(rna_file_path: Path, download_url: str) -> None:
    rna_path = pathlib.Path(rna_file_path)
    download_file = rna_file_path.with_suffix('.tar')
    if rna_path.exists():
        return None
    rna_path.mkdir(parents=True, exist_ok=True)
    if not download_file.exists():
        print("File not found. Downloading...")
        # Download the file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        with open(download_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            print("Download complete.")

    # Decompress the tar file
    print("Decompressing the tar file...")
    with tarfile.open(download_file, 'r') as tar:
        tar.extractall(path=rna_path)
    print("Decompression complete.")
