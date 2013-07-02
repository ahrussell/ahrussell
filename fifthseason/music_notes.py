import collections
from fractions import Fraction
import os

# note (D3, D#3, Db3) duration (1/4, 1/3) other (slurred, trill)

NOTES = {"R": 0, "G": 1, "G#": 2, "Ab": 2, "A": 3, "A#": 4, "Bb": 4, "B": 5, "C": 6, "C#": 7, "Db": 7, "D": 8, "D#": 9, "Eb": 9, "E": 10, "F": 11, "F#": 12}

class Note():
    def __init__(self, pitch, octave, duration, other = None):
        
        self.pitch = pitch
        self.octave = octave
        self.duration = duration
        self.abs_value = NOTES[self.pitch] + (self.octave * 12)
        
        if other != None:
            self.other = other
    
    def __repr__(self):
        return "Note: " + self.pitch + str(self.octave)


class MusicSequence(list):
    def __init__(self, file):
        
        fp = open(os.getcwd() + "/" + file, "r")
        
        lines = fp.readlines()
        
        # build keysignature
        unparsed = lines[0].split()
        time_sig = [int(unparsed[0][0]), int(unparsed[0][2])]
        key_sig = []
        
        for key in unparsed[1:]:
            key_sig.append(key)
        
        for line in lines[1:]:
                
            info = line.split()
            
            if len(info) == 0:
                continue
            
            if len(info[0]) == 3:
                pitch = info[0][:2]
                octave = int(info[0][2])
            else:
                pitch = info[0][0]
                
                for key in key_sig:
                    if pitch in key[0]:
                        pitch += key[1]
                        break
                        
                octave = int(info[0][1])
            
            duration = Fraction(info[1])
            other = []
            
            if len(info) > 2:
                other = info[2:]
            
            self.append(Note(pitch, octave, duration, other))
    
    def to_string(self):
        str = ""
        
        for note in self:
            str += note.pitch
        
        return str
    
    def relative(self):
            
        lst = []
        
        previous = self[0]
        lst.append(0)
        
        for note in self[1:]:
            lst.append(note.abs_value - previous.abs_value)
            
            previous = note
        
        return lst
    
    def to_relative_string(self):
        str = ""
        
        for val in self.relative():
            str += chr(val + 75) # 75, or 'K', is the 0 point
        
        return str
    
    def to_abs_value_string(self):
        string = ""
        
        for note in self:
            string += chr(note.abs_value+50)
        
        return string
            
"""parser = MusicParser("music/test.txt")

for measure in parser:
    for note in measure:
        print note.abs_value + str(note.duration)
    print"""