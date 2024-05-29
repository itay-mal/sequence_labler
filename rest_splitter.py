
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import os
import glob

SOURCE_FILE = "C:/Users/itaym/Documents/limudim/semester_8/robotic_hand_project/data_measurements/rest_27_05_2024_20_26_03.csv"
OUTPUT_DIR = "C:/Users/itaym/Documents/limudim/semester_8/sequence_labler/output"
LABELS = ['Up', 'Down', 'Forward', 'Back'] # TODO: generalize?
DATA_AXES = ['accX', 'accY', 'accZ', 'gyroX','gyroY','gyroZ'] # TODO: generalize?
NUM_SAMPLES = 100 # number of samples per example

def read_sample(src: os.PathLike) -> pd.DataFrame:
    return pd.read_csv(src).infer_objects()

full_data = read_sample(SOURCE_FILE)

start_idx = 0
active_label = 'Rest'

def get_next_file(base_path: os.PathLike, pattern: str) -> os.PathLike:
    idx = 0
    while True:
        p = os.path.join(base_path, pattern.format(idx))
        if not os.path.isfile(p):
            return p
        idx += 1

def save_func():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # save csv of the selected section with name like "<label>_<incremental counter>.csv"
    sample_name = get_next_file(OUTPUT_DIR, f"{active_label}_{{:04}}.csv")
    full_data[:][start_idx:start_idx+NUM_SAMPLES].to_csv(sample_name, index=None)

while(start_idx+NUM_SAMPLES<full_data.to_numpy().shape[0]):
    save_func()
    start_idx += NUM_SAMPLES
