import pretty_midi
import pandas as pd
import collections
import numpy as np
from matplotlib import pyplot as plt
from typing import Optional
import seaborn as sns


def midi_to_raw_notes(file: str) -> pd.DataFrame:
    midi_file = pretty_midi.PrettyMIDI(file)
    instrument = midi_file.instruments[0]  # sve kompozicije imaju samo grand piano kao instrument, ovo je da bi se izbegla greska
    notes = collections.defaultdict(list)
    sorted_notes = sorted(instrument.notes, key=lambda note: note.start)  # note se sortiraju po startnom vremenu
    prev_start = sorted_notes[0].start

    for note in sorted_notes:
        # za svaku notu se podaci ubacuju u listu
        start = note.start
        end = note.end
        notes['pitch'].append(note.pitch)  # real vrednost koja simbolicki predstavlja visinu note
        notes['start'].append(start)
        notes['end'].append(end)    # vrednosti predstavljaju pocetak i kraj jedne note u vremenu u sekundama
        notes['step'].append(start - prev_start)  # vremenska razlika izmedju ove i prethodne note, stepen
        notes['duration'].append(end - start)
        prev_start = start

    return pd.DataFrame({name: np.array(value) for name, value in notes.items()})


def raw_notes_to_midi(
  notes: pd.DataFrame,
  out_file: str,
  instrument_name: str,
  velocity: int = 100,  # note loudness
) -> pretty_midi.PrettyMIDI:

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=pretty_midi.instrument_name_to_program(
            instrument_name))

    prev_start = 0
    for i, note in notes.iterrows():
        start = float(prev_start + note['step'])
        end = float(start + note['duration'])
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=int(note['pitch']),
            start=start,
            end=end,
        )
        instrument.notes.append(note)
        prev_start = start

    pm.instruments.append(instrument)
    pm.write(out_file)
    return pm


def plot_piano_roll(notes: pd.DataFrame, track: str, count: Optional[int] = None):
    if count:
        title = f'First {count} notes of {track}'
    else:
        title = f'Whole {track}'
        count = len(notes['pitch'])
    plt.figure(figsize=(20, 4))
    plot_pitch = np.stack([notes['pitch'], notes['pitch']], axis=0)
    plot_start_stop = np.stack([notes['start'], notes['end']], axis=0)
    plt.plot(
      plot_start_stop[:, :count], plot_pitch[:, :count], color="b", marker=".")
    plt.xlabel('Time [s]')
    plt.ylabel('Pitch')
    _ = plt.title(title)
    plt.show()


def plot_distributions(notes: pd.DataFrame, track: str, drop_percentile=2.5):

    plt.figure(figsize=[15, 5])
    plt.subplot(1, 3, 1)
    sns.histplot(notes, x="pitch", bins=20)

    plt.subplot(1, 3, 2)
    max_step = np.percentile(notes['step'], 100 - drop_percentile)
    sns.histplot(notes, x="step", bins=np.linspace(0, max_step, 21))

    plt.subplot(1, 3, 3)
    max_duration = np.percentile(notes['duration'], 100 - drop_percentile)
    sns.histplot(notes, x="duration", bins=np.linspace(0, max_duration, 21))
    _ = plt.title(track)
    plt.show()
