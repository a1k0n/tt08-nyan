import mido
import numpy as np

H_TOTAL = 640+16+48+96
F_CLK = 25.175e6

print("virtual sample rate", F_CLK / H_TOTAL)

# Load the MIDI file
midi_file = mido.MidiFile('../nyancat.mid')

bassnote = np.zeros(288, dtype=int)
bassoct = np.zeros(288, dtype=int)
basstrigger = np.zeros(288, dtype=int)
melodynote = np.zeros(288, dtype=int)
melodyoct = np.zeros(288, dtype=int)
melodytrigger = np.zeros(288, dtype=int)

highnote = 75
lownote = 59
lasthighT = None

notes = ['C ', 'C#', 'D ', 'D#', 'E ', 'F ', 'F#', 'G ', 'G#', 'A ', 'A#', 'B ']
# Iterate through all tracks
for i, track in enumerate(midi_file.tracks):
    print(f"Track {i}: {track.name}")
    T = 0
    for msg in track:
        # Print all MIDI messages
        T += msg.time
        if msg.type == 'note_on':
            if msg.note == 90:
                # skip this note as it's used in the only chord which we can't do
                continue
            note, oct = msg.note%12, msg.note//12
            # highest note in the bassline is E5
            highdist = np.abs(msg.note - highnote)
            lowdist = np.abs(msg.note - lownote)
            print(T//96, T%96, 'note', msg.note, notes[msg.note%12], 'oct', msg.note//12, 'highdist', highdist, 'lowdist', lowdist)
            if highdist < lowdist and T != lasthighT:
                melodynote[T//96] = note
                melodyoct[T//96] = oct
                melodytrigger[T//96] = 1
                highnote = msg.note
                lasthighT = T
                if lownote > highnote:
                    lownote = highnote - 1
                print("  melody")
            else:
                bassnote[T//96] = note
                bassoct[T//96] = oct
                basstrigger[T//96] = 1
                lownote = msg.note
                if highnote < lownote:
                    highnote = lownote + 1
                print("  bass")

        if msg.type == 'end_of_track':
            print(T//96, T%96, 'end_of_track')

    print(f"Total length: {T//96} ticks")

melodynotes = set()
bassnotes = set()

for i in range(288):
    if basstrigger[i] != 1:
        bassnote[i] = bassnote[i-1]
        bassoct[i] = bassoct[i-1]
    if melodytrigger[i] != 1:
        melodynote[i] = melodynote[i-1]
        melodyoct[i] = melodyoct[i-1]
    melodynotes.add(melodynote[i])
    bassnotes.add(bassnote[i])

print("melodynotes", [notes[n] for n in sorted(list(melodynotes))])
print("bassnotes", [notes[n] for n in sorted(list(bassnotes))])

# Create a mapping for melodynotes
melody_scale = sorted(list(melodynotes))
note_to_index = {note: index for index, note in enumerate(melody_scale)}

# Function to remap notes
def remap_note(note):
    if note not in note_to_index:
        raise ValueError(f"Note {note} not in melody scale")
    return note_to_index[note]

# Remap bassnotes and melodynotes
remapped_bassnote = []
remapped_melodynote = []

for i in range(288):
    try:
        remapped_bassnote.append(remap_note(bassnote[i]))
    except ValueError as e:
        print(f"Error at index {i}: {e}")
        raise

    remapped_melodynote.append(remap_note(melodynote[i]))

# Replace original arrays with remapped versions
bassnote = np.array(remapped_bassnote, dtype=int)
melodynote = np.array(remapped_melodynote, dtype=int)

print("Remapped melody scale:", [notes[n] for n in melody_scale])
print("Number of unique notes after remapping:", len(melody_scale))

def freqinc(freq):
    # inc * F_CLK / H_TOTAL / (1<<regsize) = freq
    # inc = freq * (1<<regsize) * H_TOTAL / F_CLK
    return round(freq * (1<<14) * H_TOTAL / F_CLK)

def noteinc(noteidx):
    freq = 110 * 2**((noteidx+3)/12)
    return freqinc(freq)
  
print("melody increment table", ' '.join(["%02x" % noteinc(n) for n in melody_scale]))

def writehex(name, data, pad=0):
    with open('../data/' + name, 'w') as f:
        f.write(" ".join(["%01x" % n for n in data]))
        # fill out to 512 entries with x's
        for _ in range(pad - len(data)):
            f.write(' x')
        f.write('\n')


writehex("bassnote.hex", bassnote, pad=512)
writehex("bassoct.hex", bassoct - np.min(bassoct), pad=512)
writehex("basstrigger.hex", basstrigger, pad=512)
writehex("melodynote.hex", melodynote, pad=512)
writehex("melodyoct.hex", melodyoct - np.min(melodyoct), pad=512)
writehex("melodytrigger.hex", melodytrigger, pad=512)

writehex("noteinc.hex", [noteinc(n) for n in melody_scale])

print("bassnote", ' '.join(map(str, bassnote)))
print("bassoct", ' '.join(map(str, bassoct - np.min(bassoct))))
print("basstrigger", ' '.join(map(str, basstrigger)))
print("melodynote", ' '.join(map(str, melodynote)))
print("melodyoct", ' '.join(map(str, melodyoct - np.min(melodyoct))))
print("melodytrigger", ' '.join(map(str, melodytrigger)))
