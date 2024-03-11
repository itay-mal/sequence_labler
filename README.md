# Sequence Labler

Visually tagging and aligning sequences of data - as preperation to sequential ML training.

## Usage

- Set `SOURCE_FILE` to the data measurements file (currently only csv is supported).  
- Set `OUTPUT_DIR` to the folder where labeled samples will be dumped to
  - make sure write permissions for selected directory.  
  - if directory does not exist the script will try to create it.
- Set `LABELS` to contain the required labels (classes).  
- Set `DATA_AXES` to contain the relevant data fetures - headers from the input data file.  
- Use `-10`, `-1` `+1` and `+10` to locate the translate the sample to wanted position, select the relevant label and click `Save` when satisfied, the sliced sample will be eported to `<OUPUT_DIR>/<label>_<incremental counter>.csv`  
