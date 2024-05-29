
#------------------------------------------------------------------------------#
# simple pyplot based GUI to export tagged data sequences 
#------------------------------------------------------------------------------#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import os
import glob

SOURCE_FILE = "C:/Users/itaym/Documents/limudim/semester_8/robotic_hand_project/data_measurements/up_28_03_2024_18_12_59.csv"
OUTPUT_DIR = "C:/Users/itaym/Documents/limudim/semester_8/sequence_labler/output"
LABELS = ['Up', 'Down', 'Forward', 'Back'] # TODO: generalize?
DATA_AXES = ['accX', 'accY', 'accZ', 'gyroX','gyroY','gyroZ'] # TODO: generalize?
NUM_SAMPLES = 100 # number of samples per example
start_idx = 0
buttons_background = 'lightgoldenrodyellow'

def read_sample(src: os.PathLike) -> pd.DataFrame:
    return pd.read_csv(src).infer_objects()

full_data = read_sample(SOURCE_FILE)

fig, ax = plt.subplot_mosaic([
    ['main',           'main',          'main',        'main',          'axes'          ],
    ['main',           'main',          'main',        'main',          'label'         ],
    ['back_10_button', 'back_1_button', 'save_button', 'next_1_button', 'next_10_button']
], width_ratios=[1,1,1,1,1],
height_ratios=[4,4,1],
layout='constrained')

ax['axes'].set_facecolor(buttons_background)
axes_radio = RadioButtons(ax['axes'], DATA_AXES, active=0)
active_axes = DATA_AXES[0] # TODO: needed?

ax['label'].set_facecolor(buttons_background)
label_radio = RadioButtons(ax['label'], LABELS, active=0)
active_label = LABELS[0]

def get_next_file(base_path: os.PathLike, pattern: str) -> os.PathLike:
    idx = 0
    while True:
        p = os.path.join(base_path, pattern.format(idx))
        if not os.path.isfile(p):
            return p
        idx += 1

def get_reference(base_path: os.PathLike, label: str) -> None | str:
    candidates = glob.glob(os.path.join(base_path,f"{label}*"))
    if len(candidates):
        return sorted(candidates)[0]
    return None

def axesfunc(label):
    global active_axes
    active_axes = label
    update_plot()
    fig.canvas.draw()
axes_radio.on_clicked(axesfunc)

def labelfunc(label):
    global active_label
    active_label = label
    update_plot()
label_radio.on_clicked(labelfunc)

back_10_button = Button(ax['back_10_button'], '-10')
def back_10_func(event):
    global start_idx
    start_idx -= 10
    update_plot()
back_10_button.on_clicked(back_10_func)

back_1_button = Button(ax['back_1_button'], '-1')
def back_func(event):
    global start_idx
    start_idx -= 1
    update_plot()
back_1_button.on_clicked(back_func)

save_button = Button(ax['save_button'], 'Save')
def save_func(event):
    # TODO: speculatively create output dir at the begining of script?
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # save csv of the selected section with name like "<label>_<incremental counter>.csv"
    sample_name = get_next_file(OUTPUT_DIR, f"{active_label}_{{:04}}.csv")
    full_data[:][start_idx:start_idx+NUM_SAMPLES].to_csv(sample_name, index=None)
    update_plot()
save_button.on_clicked(save_func)

next_1_button = Button(ax['next_1_button'], '+1')
def next_func(event):
    global start_idx
    start_idx += 1
    update_plot()
next_1_button.on_clicked(next_func)

next_10_button = Button(ax['next_10_button'], '+10')
def next_10_func(event):
    global start_idx
    start_idx += 10
    update_plot()
next_10_button.on_clicked(next_10_func)

data_line, = ax['main'].plot([1,2,3],[0,4,0], label='Data')
ref_line,  = ax['main'].plot([],[], label='Reference')

def update_plot():
    data_line.set_xdata(range(start_idx,start_idx+NUM_SAMPLES))
    data_line.set_ydata(full_data[active_axes][start_idx:start_idx+NUM_SAMPLES])
    ref_csv = get_reference(OUTPUT_DIR, active_label)
    if ref_csv:
        ref_data = read_sample(ref_csv)
        ref_line.set_xdata(range(start_idx,start_idx+NUM_SAMPLES))
        ref_line.set_ydata(ref_data[active_axes][:NUM_SAMPLES])
    else:
        ref_line.set_xdata([])
        ref_line.set_ydata([])

    data_bbox = ref_line.get_bbox()
    ref_bbox = ref_line.get_bbox()
    ax['main'].set_xlim(start_idx,start_idx+NUM_SAMPLES) # this does not change
    # TODO: feels inefficient :(
    ax['main'].set_ylim(np.min([*data_line.get_ydata(), *ref_line.get_ydata()]),
                        np.max([*data_line.get_ydata(), *ref_line.get_ydata()]))
    fig.canvas.draw()

ax['main'].legend()
update_plot()

plt.show()
