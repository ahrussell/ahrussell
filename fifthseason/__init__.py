# parse music/create training data
# create markov chain
    # find patterns
# compose music

# first season theme(s)
    # transition: first + second as training
# second theme(s)
    # trans
# third theme(s)
    # trans
# fourth theme(s)

import suffix_tree
from music_notes import MusicSequence, Note
import os
import markov
import random
from fractions import Fraction
import json
import suffix_tree
from math import pow

# notes and their "absolute values"
NOTES = {"R": 0, "G": 1, "G#": 2, "Ab": 2, "A": 3, "A#": 4, "Bb": 4, "B": 5, "C": 6, "C#": 7, "Db": 7, "D": 8, "D#": 9, "Eb": 9, "E": 10, "F": 11, "F#": 12}

class ComposerBot:

    def __init__(self, files):
        self.train(files)

    def train(self, files):
        self.order = 1 # first order markov chain....do not change from 1
        self.chains = [markov.MarkovChain()]
        self.seqs = []
        
        # parse music
        for name,file in files.iteritems():
            fp = open(os.getcwd() + "/" + file, "r")
            
            self.seqs.append(MusicSequence(file))
          
            fp.close()
        
        patterns = [] # uncompressed patterns
        compressed = []
        
        # extract patterns
        for seq in self.seqs:
            abs_str = seq.to_abs_value_string()
            stree = suffix_tree.SuffixTree(abs_str)
            
            tree_patterns = stree.get_patterns(3)
            
            for p in tree_patterns:
                durations = []
                
                for note in seq[p[0]-1:p[0]+p[1]+1]:
                    durations.append(note.duration)
                
                try:
                    patterns.append({"seq": seq, "start_index": p[0],"depth": p[1],"start_note": seq[p[0]],"end_note": seq[p[0]+p[1]+1], "durations": durations})
                except IndexError:
                    patterns.append({"seq": seq, "start_index": p[0],"depth": p[1],"start_note": seq[p[0]],"end_note": seq[p[0]+p[1]], "durations": durations})
        
        patterns = self.compress_patterns(patterns)
        
        for seq in self.seqs:
            self.add_to_markov_chain(self.chains[0], seq, 1)
        
        for pattern in patterns:
            self.insert_pattern(pattern)
            
    def insert_pattern(self, pattern):
        
        # create state from pattern
        seq = pattern["seq"]
        key = []
        
        for note in seq[pattern["start_index"]:pattern["start_index"]+pattern["depth"]]:
            key.append((note.pitch, note.octave, note.duration))
        
        key = tuple(key)
        
        try:
            self.chains[0][key] 
        except KeyError:
            self.chains[0][key] = State()
        
        # get ending note
        # add ending note to pattern state
    
        try:
            end_note = seq[pattern["start_index"]+pattern["depth"]]
            
            self.chains[0][key].add_side((end_note.pitch, end_note.octave, end_note.duration))
        except KeyError:
            pass
        
        # get prior note
        # find prior note in chain
        # weight pattern and add to prior note state
            # add state to chain
        try:
            prior_note = seq[pattern["start_index"]-1]
            
            for i in range(len(key)):
                self.chains[0][(prior_note.pitch, prior_note.octave, prior_note.duration)].add_side(key)
        except KeyError:
            pass
    
    def compress_patterns(self, patterns):
        comps = {}
        
        deletions = []
        
        for seq in self.seqs:
            abs_str = seq.to_abs_value_string()
            
            for x in [p for p in patterns if p["seq"] == seq]:
                try:
                    comps[abs_str[x["start_index"]:x["start_index"]+x["depth"]]] +=1
                except KeyError:
                    comps[abs_str[x["start_index"]:x["start_index"]+x["depth"]]] = 1
        
        for k,c in comps.iteritems():
            if c < 2 or k=='':
                deletions.append(k)
        
        for k in deletions:
            del comps[k]
        
        final = []
        
        for seq in self.seqs:
            abs_str = seq.to_abs_value_string()
            
            final += [p for p in patterns if p["seq"] == seq and abs_str[p["start_index"]:p["start_index"]+p["depth"]] in comps.keys()]
        
        return final
    
    def add_to_markov_chain(self, chain, seq, order):
        
        if order > len(seq):
            order = len(seq)
        
        for i in range(0, len(seq) - (order + 1)):
            pitches = []
            octaves = []
            durations = []
            
            for j in range(0, order):
                pitches.append(seq[i+j].pitch)
                octaves.append(seq[i+j].octave)
                durations.append(seq[i+j].duration)
            
            next_pitch = seq[i+order].pitch
            next_octave = seq[i+order].octave
            next_duration = seq[i+order].duration
            
            key = []
            
            for k in range(0,len(pitches)):
                key.append((pitches[k],octaves[k],durations[k]))
            
            key = tuple(key)

            try:
                chain[key[0]]
            except KeyError:
                chain[key[0]] = State()
            
            chain[key[0]].add_side((next_pitch, next_octave, next_duration))
        return chain
    
    def write(self, number_of_notes):
        # get rand starting note or starting pattern (random state)
        
        def rand_start_state():
            seq = self.seqs[random.randint(0, len(self.seqs)-1)]
            note = seq[0]
            key = (note.pitch, note.octave, note.duration)
            
            return key
        
        def next_note(order):
            order -= 1

            new_state = self.chains[order].next()
            
            try:
                new_state[0]
                
                return new_state
            except TypeError:
                print new_state
                exit("fail")
                    
                return next_note(order)
        
        start = rand_start_state()
        states = [tuple([tuple([start[0],start[1],start[2]])])]
        piece = []
        
        self.chains[0].set_current_state(states[0][0])
        
        # create beginning of sentence
        for note in states[len(states) -1]:
            piece.append(list(note))

        piece = piece[1:]
        leng = 0
        
        while True:
            new_note = next_note(self.order)
            
            self.chains[0].set_current_state(new_note)
            
            piece.append(list(new_note))
            
            if type(new_note[0]) == type("string"):
                leng += 1
            else:
                leng += len(new_note)
            
            if leng > number_of_notes:
                break
        
        # flatten piece
        flattened = []
        
        for notes in piece:
            if type(notes[0]) == type("string"):
                flattened.append(notes)
            else:
                for note in notes:
                    flattened.append(list(note))
        
        return flattened
    
    def measurify(self, piece, top, bot):
        multiplier = bot / 4
        for note in piece:
            note[2] *= multiplier

        leftover = None
        measures = []
        count = Fraction(0)
        i = 0
        
        for note in piece:
            try:
                measures[i]
            except IndexError:
                measures.append([])
                
            if leftover != None:
                measures[i].append((leftover[0], leftover[1], float(leftover[2].numerator) / leftover[2].denominator))
                count += leftover[2]
            
            count += note[2]
            
            if count > Fraction(top / bot):
                leftover = (note[0], note[1], count % 1)
                
                measures[i].append((note[0], note[1], float((note[2] - leftover[2]).numerator) / (note[2] - leftover[2]).denominator))
                count = 1
            else:
                measures[i].append((note[0], note[1], float(note[2].numerator) / note[2].denominator))
                leftover = None
            
            count = count % 1
            
            if count == 0:
                i += 1
                            
        return measures
            
        
'''if __name__=="__main__":
    pieces = {"spring": "music/spring.txt", "summer": "music/summer.txt", "autumn": "music/autumn.txt", "winter": "music/winter.txt"}
    
    for piece, file in pieces.iteritems():
        bot = ComposerBot({piece: file})
        markov_piece = bot.measurify(bot.write(350), 4, 4)
        
        fp1 = open("/Applications/MAMP/htdocs/ID1/json/" + piece + ".json", "w")
        fp2 = open("json/" + piece + ".json", "w")
        
        json.dump(markov_piece, fp1)
        json.dump(markov_piece, fp2)
        
        fp1.close()
        fp2.close()
    
    bot = ComposerBot(pieces)
    piece = bot.measurify(bot.write(350), 4, 4)
    
    fp1 = open("/Applications/MAMP/htdocs/ID1/json/fifth_season.json", "w")
    fp2 = open("json/fifth_season.json", "w")
    
    json.dump(piece, fp1)
    json.dump(piece, fp2)
    
    fp1.close()
    fp2.close()'''