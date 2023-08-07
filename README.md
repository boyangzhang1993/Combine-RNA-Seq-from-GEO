# Combine RNA-Seq data from GEO Database
## Run bash:
chmod +x run_scripts.sh

./run_scripts.sh

## Inputs:
1. Download url
2. File saving path 

## Assumptions:
1. "GSM" is used as a prefix of the sample name. 
2. Additional experiment identifiers are following the "GSM" such as "B9053" and "WT-HSC-TET2-HM-DIR"
3. "TPM" is the gene expression data which is recorded in 'quant.sf'
4. The 'quant.sf' use '\t' as spliter. 

## Auto checks (derisk):
1. Check for gene names are consistent across files
2. After generating combined data, check numbers are matching with the original files. 


## Output:
Combined_RNA_TPM(from_Salmon).csv
1. genes (rows) by samples (columns) containing the RNA-Seq read counts (TPM)
2. Please note the RNA data were already processed using Salmon as stated in https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223695

