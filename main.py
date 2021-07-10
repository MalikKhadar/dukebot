# powered by Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
#   Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
#   Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
#   In International Conference on Learning Representations, 2019.

import pretty_midi
from midi import chunk_midi
from battle import battle



b = battle.Battle()
while(True):
    b.host_battle()

# saving = chunk_midi.Chunk_Saving("midi/maestro-v3.0.0/", "0", "midi/chunks/")
# params = chunk_midi.Chunk_Params(saving)
# chunk_midi.chunks_from_directory(params)

#def generate_chunks

#first file in the dataset
# midi_path = "train/mega8_9.midi"

# #access piano data
# midi_data = pretty_midi.PrettyMIDI(midi_path)
#midi_tools.chunks_from_directory("maestro-v3.0.0/", 4, 4, "chunks/")
# piano = midi_data.instruments[0]
# piano_roll = piano.get_piano_roll()
# quantized = midi_tools.piano_roll_to_pretty_midi(piano_roll, 100)
# quantized.write("q_test.midi")
#midi_tools.chunkify_midi(midi_data, 2, 8, "train/", "mega8_")


# chunk = []

# print("duration:",midi_data.get_end_time())
# print(f'{"note":>10} {"start":>10} {"end":>10}')
# for instrument in midi_data.instruments:
#     print("instrument:", instrument.program)
#     for note in instrument.notes:
#         if note.start < 5:
#             print(f'{note.pitch:10} {note.start:10} {note.end:10}')
#             chunk.append(note)
# test = pretty_midi.Instrument(program=0)
# midi_tools.populate_instrument(test, chunk)
# roll = test.get_piano_roll()
# pm = midi_tools.piano_roll_to_pretty_midi(roll)
# pm.write("q_test.midi")
#q = quantize(pm, 2)
#pm.write("q_test.midi")
# #get number of midi_chunks
# track_length = midi_data.get_end_time()
# chunk_length = 5    #each chunk lasts ~5 seconds
# num_chunks = int(track_length/chunk_length)

# tc = midi_data.get_tempo_changes()
# midi_data.
# for c in tc:
#     print(c)
# #set fps/quantize
# bpm = midi_data.estimate_tempo()
# bps = bpm/60        #get beats per second
# notes_per_beat = 3  #will be (4*val)ths in 4/4
# notes_per_second = bps*notes_per_beat

# print(notes_per_second)
# piano_roll = piano.get_piano_roll(fs=notes_per_second)

# quantized = midi_tools.piano_roll_to_pretty_midi(piano_roll, notes_per_second)
# quantized.write("q_test.midi")


# sampleRate = 44100
# waves = midi_data.synthesize(sampleRate, signal.sawtooth)
# # Convert to (little-endian) 16 bit integers.
# audio = (waves * (2 ** 15 - 1)).astype("<h")
# with wave.open("sound2.wav", "w") as f:
#     # 2 Channels.
#     f.setnchannels(2)
#     # 2 bytes per sample.
#     f.setsampwidth(2)
#     f.setframerate(sampleRate)
#     f.writeframes(audio.tobytes())
# piano = midi_data.instruments[0]