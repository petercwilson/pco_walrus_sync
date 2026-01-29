from midiutil import MIDIFile
import io

def create_midi_file(songs):
    midi = MIDIFile(1)
    time = 0

    midi.addTrackName(0, 0, "Celebration Service")
    midi.addTempo(0, 0, 120)

    for i, song in enumerate(songs):
        midi.addProgramChange(0, 0, time, i)
        time += 1

    buffer = io.BytesIO()
    midi.writeFile(buffer)
    buffer.seek(0)
    return buffer
