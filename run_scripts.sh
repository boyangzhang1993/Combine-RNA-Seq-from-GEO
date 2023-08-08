#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Install required packages from requirements.txt
pip install -r requirements.txt

# Run the python scripts
python data_process.py
python data_checker.py
python mapping_transcripts_id_name_human_homolog.py
# Deactivate the virtual environment
deactivate