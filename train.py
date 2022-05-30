import pathlib
import glob
import pandas as pd
import numpy as np
import tensorflow as tf
from util import midi_to_raw_notes
import config as cfg

data_dir = pathlib.Path(cfg.data_directory)  # path do dataseta
filenames = glob.glob(str(data_dir / '**/*.mid*'))
num_files = 5
all_notes = []
for f in filenames[:num_files]:
    notes = midi_to_raw_notes(f)
    all_notes.append(notes)

all_notes = pd.concat(all_notes)

n_notes = len(all_notes)
print('Number of notes parsed:', n_notes)

key_order = ['pitch', 'step', 'duration']
train_notes = np.stack([all_notes[key] for key in key_order], axis=1)

notes_ds = tf.data.Dataset.from_tensor_slices(train_notes)
notes_ds.element_spec

