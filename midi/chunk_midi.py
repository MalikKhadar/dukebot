#source: https://github.com/haryoa/note_music_generator
import glob
import midi.midi_tools as midi
import pretty_midi

class Chunk_Length:
    '''specify length of chunks and loops'''
    def __init__(self, min_notes=5, chunk_length=4, 
                 notes_per_beat=4, loops=4):
        self.min_notes = min_notes
        self.chunk_length = chunk_length
        self.notes_per_beat = notes_per_beat
        self.loops = loops

class Chunk_Cleaning:
    '''specify how orignial midi is cleaned'''
    def __init__(self, highest_notes=True, remove_overlap=True,
                 deletion=False, trim_chunk=True):
        self.highest_notes = highest_notes
        self.remove_overlap = remove_overlap
        self.deletion = deletion
        self.trim_chunk = trim_chunk
        
class Chunk_Saving:
    '''specify source of midi and dest of chunks'''
    def __init__(self, dir, prefix, dest):
        self.dir = dir
        self.prefix = prefix
        self.dest = dest

class Chunk_Params:
    '''holds all chunk specifications'''
    def __init__(self, saving, length=Chunk_Length(), 
                 cleaning=Chunk_Cleaning()):
        self.saving = saving
        self.length = length
        self.cleaning = cleaning

def save_chunk(chunk, params, f_index, file_prefix="0"):
    '''cleans and saves chunk per params'''
    if params.cleaning.highest_notes:
        chunk = midi.highest_notes(chunk)
    if params.cleaning.remove_overlap:
        chunk = midi.remove_overlap(chunk, params)
    chunk = midi.bind_notes(chunk, params.cleaning.volume)
    if params.cleaning.trim_chunk:
        chunk = midi.trim_chunk(chunk, params)
    #only use long chunks
    if len(chunk) >= params.length.min_notes:
        if midi.assert_length(chunk, params):
            chunk = midi.loop_chunk(chunk, params)
            midi.save_midi(chunk, params, file_prefix, f_index)

def chunkify_midi(midi_data, params):
    '''writes chunks of instrument 0 to dest'''
    #access piano data
    piano = midi_data.instruments[0]
    chunks = [[]]
    chunk_offset = piano.notes[0].start
    #split notes into chunks list
    for note in piano.notes:
        #create new chunk if necessary
        cutoff = len(chunks)*params.length.chunk_length
        if note.start > cutoff:
            chunks.append([])
            chunk_offset = note.start
        #align note, use bounded vals
        start = note.start - chunk_offset
        s = midi.quantized(start, params)
        end = note.end - chunk_offset
        e = midi.quantized(end, params)
        new_note = pretty_midi.Note(
            velocity = note.velocity,
            pitch = note.pitch,
            start = s,
            end = e
        )
        chunks[-1].append(new_note)
    return chunks

def create_chunks(midi_path, params, file_prefix):
    '''takes midi from path, chunkifies, writes to dest'''
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    chunks = chunkify_midi(midi_data, params)
    #write each chunk to dest
    f_index = 0
    for chunk in chunks:
        save_chunk(chunk, params, f_index, file_prefix)
        #give each file unique name
        f_index += 1

def chunks_from_directory(params):
    '''create chunks from directory (recursively)'''
    #only act on midi files
    prefix = 0
    midi_dir = params.saving.dir + '**/*.midi'
    for filename in glob.iglob(midi_dir, recursive=True):
        #iterate file prefixes to avoid overwrites
        print("Chunkifying " + filename)
        create_chunks(filename, params, str(prefix)+"_")
        prefix += 1