import glob
import pathlib
import pretty_midi
import config as cfg
from util import midi_to_raw_notes, plot_piano_roll, plot_distributions

data_dir = pathlib.Path(cfg.data_directory)  # path do dataseta
filenames = glob.glob(str(data_dir / '**/*.mid*'))  # lista svih fajlova od svih autora
sample_file = filenames[50]  # random fajl za ispitivanje
midi_file = pretty_midi.PrettyMIDI(sample_file)  # ucitavanje MIDI fajla u objekat
raw_notes = midi_to_raw_notes(midi_file)    # iz util.py


def print_file_data(head):
    print('\n\n\nNumber of files:', len(filenames))
    for i in range(head):
        print(filenames[i])


def print_song_details():
    print('\n\n\nSample song name: ', sample_file)
    print('Number of instruments:', len(midi_file.instruments))
    instrument = midi_file.instruments[0]
    instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
    print('Instrument name:', instrument_name)
    print('\n\n')
    for i, note in enumerate(instrument.notes[:10]):
        note_name = pretty_midi.note_number_to_name(note.pitch)  # iz simbolicke num vrednosti u muzicku notaciju npr C5
        duration = note.end - note.start
        print(f'{i}: pitch={note.pitch}, note_name={note_name},'
              f' duration={duration:.4f}')


print_file_data(10)
print_song_details()
print('\n\n\nFirst 10 raw notes sorted by start time')
print(raw_notes.head(10))
plot_piano_roll(raw_notes, sample_file, 100)  # plot prvih 100 nota po visini kroz vreme
plot_distributions(raw_notes, sample_file)  # plot histogram za parametre treniranja: visina tona, stepen, trajanje
