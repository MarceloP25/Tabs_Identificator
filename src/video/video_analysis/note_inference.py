# note_inference.py

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]

STANDARD_TUNING = {
    0: ("E", 40),  # Mizão
    1: ("A", 45),
    2: ("D", 50),
    3: ("G", 55),
    4: ("B", 59),
    5: ("E", 64)   # Prima
}


def midi_to_note(midi):
    return NOTE_NAMES[midi % 12]


def infer_notes_from_pressure(pressure_map, tuning=STANDARD_TUNING):
    """
    Entrada:
      pressure_map[string_id] = list of pressed frets

    Saída:
      notes[string_id] = {
        fret: int or None,
        midi: int,
        note: str
      }
    """

    notes = {}

    for string_id, (open_note, open_midi) in tuning.items():
        pressed_frets = pressure_map.get(string_id, [])

        if not pressed_frets:
            fret = None
            midi = open_midi
        else:
            fret = max(pressed_frets)
            midi = open_midi + fret

        notes[string_id] = {
            "fret": fret,
            "midi": midi,
            "note": midi_to_note(midi)
        }

    return notes
