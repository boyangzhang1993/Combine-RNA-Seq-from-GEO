import gzip
from pathlib import Path
import tempfile
import pandas as pd
from data_process import TRANSCRIPT_OUTPUT

from utility import custom_aggregator



# Path for files
BIOMART_PATH = Path("./biomart_mapping/mart_human.txt.gz")
TRANSCRIPT_PATH = Path(f"./{TRANSCRIPT_OUTPUT}")
MAPPING_OUT = "merged_output"
# Constants for accessing column names
CONFIDENCE_LOW_HIGH = 'Human orthology confidence [0 low, 1 high]'
JOIN_METHOD = "left"
ID_TRANSCRIPT = "Name"
HUMAN_GENE_NAME = 'Human gene name'
STABLE_ID_VERSION = "Transcript stable ID version"

# Check if the .gz file exists
if not BIOMART_PATH.exists():
    raise FileNotFoundError(f"{BIOMART_PATH} does not exist")

# Reading the transcript dataset
df_transcript = pd.read_csv(TRANSCRIPT_OUTPUT)

# Create a temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    # Decompress the gz file into the temp directory
    txt_path = Path(temp_dir) / BIOMART_PATH.stem  # Assuming the result is a .txt file

    with gzip.open(BIOMART_PATH, 'rb') as f_in:
        with open(txt_path, 'wb') as f_out:
            f_out.write(f_in.read())

    # Read the contents of the decompressed txt file using pandas
    df_name_homolog = pd.read_csv(txt_path)  # Adjust based on the format of your txt file

    #
    # # Performing a left join
    # df_transcript[ID_TRANSCRIPT] = df_transcript[ID_TRANSCRIPT].astype(pd.StringDtype())
    merged_df = df_name_homolog.merge(df_transcript, left_on=STABLE_ID_VERSION, right_on=ID_TRANSCRIPT, how=JOIN_METHOD)
    # Filter by orthology confidence
    filtered_df = merged_df[merged_df[CONFIDENCE_LOW_HIGH] == 1]
    # Grouping by 'group_col' and applying custom aggregation
    for column in filtered_df.columns:
        if column.startswith('GSM'):
            # Convert to numeric using .loc and handle errors by setting them as NaN
            filtered_df.loc[:, column] = pd.to_numeric(filtered_df[column], errors='coerce')
        else:
            filtered_df.loc[:, column] = filtered_df[column].astype(str)

    aggregated_df = filtered_df.groupby(HUMAN_GENE_NAME).agg(custom_aggregator).reset_index()
    if aggregated_df[STABLE_ID_VERSION].to_string() != aggregated_df[ID_TRANSCRIPT].to_string():
        raise ValueError
    
    columns_keep = [HUMAN_GENE_NAME, STABLE_ID_VERSION]
    columns_keep.extend([col for col in aggregated_df.columns if col.startswith('GSM')])
    # print(merged_df.head())
    merged_df.to_csv(f"./biomart_mapping/{MAPPING_OUT}.csv", index=False)
    filtered_df.to_csv(f"./biomart_mapping/{MAPPING_OUT+'_filtered'}.csv", index=False)
    aggregated_df[columns_keep].to_csv(f"./biomart_mapping/{MAPPING_OUT+'_filtered_aggregated'}.csv", index=False)
