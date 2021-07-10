import pretty_midi
import numpy as np
from scipy import signal
import wave

def piano_roll_to_pretty_midi(piano_roll, fs=100, program=0):
    '''Convert a Piano Roll array into a PrettyMidi object'''
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm

def populate_instrument(instrument, notes):
    '''puts notes in instrument'''
    for note in notes:
        instrument.notes.append(note)
    return instrument

def bound(val, lower=0, upper=None):
    '''confines val between bounds'''
    if upper == None:
        #just check lower bound
        return val if val > lower else lower
    if val > upper:
        return upper
    if val < lower:
        return lower
    return val

def quantized(n, params):
    '''returns n rounded to nearest 1/precision'''
    precision = params.length.notes_per_beat
    q = np.round(n * precision) / precision
    return q

def highest_note(notes):
    '''returns highest note from chord'''
    highest = notes[0]
    for note in notes:
        #compare pitches
        if note.pitch > highest.pitch:
            highest = note
    return highest

def highest_notes(chunk):
    '''filter non-highest notes from chunk'''
    #sort chunk based on note starts
    chunk.sort(key=lambda note: note.start)
    chords = [[chunk[0]]]
    prev_start = chunk[0].start
    #assemble chords from sorted chunk
    for note in chunk[1:]:
        if note.start != prev_start:
            chords.append([note])
            prev_start = note.start
        else:
            chords[-1].append(note)
    #return highest note in each chord
    return [highest_note(chord) for chord in chords]
        
def remove_overlap(chunk, params):
    '''removes overlapping notes'''
    new_chunk = [chunk[0]]
    #create new chunk, check endings vs starts
    for note in chunk[1:]:
        if note.start > new_chunk[-1].end:
            #only add note if start > end 
            new_chunk.append(note)
        elif not params.cleaning.deletion:
            #shorten prev note
            new_chunk[-1].end = note.start
            new_chunk.append(note)
    return new_chunk

def assert_length(chunk, params):
    '''Makes sure chunk is length beats long'''
    if chunk[-1].end < params.length.chunk_length/2 - 1:
        return False
    return True

def trim_chunk(chunk, params):
    '''Trims extra notes or note length'''
    new_chunk = []
    beats = params.length.chunk_length
    for note in chunk:
        #disclude notes that start after beats
        if note.start < beats/2:
            #trim endings of notes if needed
            note.end = bound(note.end, 0, beats/2)
            new_chunk.append(note)
    return new_chunk

def loop_chunk(chunk, params):
    '''Loops chunk, beats per loop = beats in chunk'''
    looped = []
    for loop in range(params.length.loops):
        for note in chunk:
            #copy notes with loop offset
            offset = params.length.chunk_length/2 * loop
            new_note = pretty_midi.Note(
                velocity = note.velocity,
                pitch = note.pitch,
                start = note.start + offset,
                end = note.end + offset
            )
            looped.append(new_note)
    return looped

def bind_notes(notes):
    '''ensures notes don't have corrupted values'''
    for note in notes:
        note.pitch = int(bound(note.pitch, 0, 127))
        note.velocity = int(bound(note.velocity, 0, 127))
        note.start = bound(note.start, 0)
        note.end = bound(note.end, 0)
    return notes 

def make_midi(path):
    '''returns pretty midi from path'''
    return pretty_midi.PrettyMIDI(path)

def save_midi(chunk, params, file_prefix, f_index):
    '''save midi to dest as prefix + f_index'''
    #create instrument to hold notes
    instr = pretty_midi.Instrument(program=0)
    instr = populate_instrument(instr, chunk)
    #make piano roll, pm, then save
    roll = instr.get_piano_roll()
    pm = piano_roll_to_pretty_midi(roll)
    min_notes_looped = params.length.min_notes * params.length.loops
    if len(pm.instruments[0].notes) >= min_notes_looped:
        path = params.saving.dest + file_prefix + str(f_index)
        pm.write(path + ".midi")
        
def make_wav(midi, sampleRate=44100):
    '''synthesizes midi to wav'''
    waves = midi.synthesize(sampleRate, signal.sawtooth)
    # Convert to (little-endian) 16 bit integers.
    audio = (waves * (2 ** 15 - 1)).astype("<h")
    return audio

def save_wav(wav, dest, sampleRate=44100):
    '''saves wav to dest'''
    with wave.open(dest, "w") as f:
        # 2 Channels.
        f.setnchannels(2)
        # 2 bytes per sample.
        f.setsampwidth(2)
        f.setframerate(sampleRate)
        f.writeframes(wav.tobytes())