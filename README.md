# Combine RNA-Seq Data from GEO Database
## Run bash:
chmod +x run_scripts.sh

./run_scripts.sh

## Inputs:
1. Download url
2. File saving path 

## Assumptions:
1. "GSM" is used as a prefix of the sample name. 
2. Additional experiment identifiers are following the "GSM" such as "B9053" and "WT-HSC-TET2-HM-DIR".
3. "TPM" is the gene expression data which is recorded in 'quant.sf'.
4. The 'quant.sf' use '\t' as spliter. 

## Auto checks (derisk):
1. Check for gene names are consistent across files.
2. After generating combined data, check numbers are matching with the original files. 

## Mapping ID to Gene Name and Human Homolog
1. Use Biomart mapping with the GRCm38 assembly since the "Salmon index and decoys were generated using the GRCm38/mm10 assembly". Reference: [GSM6974520](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6974520).
2. Access Biomart (version 102, GRCm38.p6) at the following [link](http://nov2020.archive.ensembl.org/index.html).
2. Filter transcripts based on the Human orthology confidence level: [0 for low, 1 for high].
3. Group (and sum) the transcripts that have identical Human Gene Names.


## Output:
Combined_RNA_TPM(from_Salmon).csv
1. Genes (rows) by samples (columns) containing the RNA-Seq read counts (TPM).
2. Please note the RNA data were already processed using Salmon as stated in https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223695.

