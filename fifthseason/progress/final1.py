import os
import markov
import random
from music_notes import MusicSequence, Note
from fractions import Fraction
import json

class ComposerBot:

    def __init__(self, *args):
        self.train(*args)

    def train(self, *args):
        self.order = 3
        files = args
        self.chains = []
        self.seqs = []
        
        for file in files:
            fp = open(os.getcwd() + "/" + file, "r")
            
            self.seqs.append(MusicSequence(file))
            
            for i in range(0, self.order):
                try:
                    self.chains[i]
                except:
                    self.chains.append(markov.MarkovChain())
            
                self.add_to_markov_chain(self.chains[i], self.seqs[len(self.seqs) - 1], i+1)
          
            fp.close()
    
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
                chain[key]
            except KeyError:
                chain[key] = State()
            
            chain[key].add_side((next_pitch, next_octave, next_duration))
        return chain
    
    def write(self):
        def rand_start_seq():
            seq = self.seqs[random.randint(0, len(self.seqs)-1)]
            key = []
            
            for i in range(self.order):
                note = seq[i]
                key.append((note.pitch, note.octave, note.duration))
            
            key = tuple(key)
                
            states = []
            
            for i in range(1, self.order+1):
                states.append(self.chains[i-1].set_current_state(key[self.order-i:]))
            
            return states
        
        def update_states(states, latest_note):
            new_states = []
            
            # update array
            for state in states:
                new_state = []
                
                for i in range(1,len(state)):
                    new_state.append(state[i])
                
                new_state.append(latest_note)
                
                new_states.append(tuple(new_state))
            
            # update markov chain
            for i in range(0, self.order):
                self.chains[i].set_current_state(new_states[i])
            
            return new_states
        
        def next_note(order):
            order -= 1

            new_state = self.chains[order].next()
            
            try:
                new_state[0]
                
                return new_state
            except TypeError:
                if order == 0:
                    bad = True
                    i = 0
                    
                    while bad:
                        if i > 5:
                            bad = False
                            break
                            
                        i += 1
                        rand_state = [key for key in self.chains[order].keys() if key[0][1] == self.chains[order].state[0][1]]
                        
                        new_state = random.choice(rand_state)
                    
                    return new_state[0]
                    
                return next_note(order)
        
        
        states = rand_start_seq()
        piece = []
        
        # create beginning of sentence
        for note in states[len(states) -1]:
            piece.append(list(note))
        piece = piece[1:]
        leng = 0
        
        while True:
            new_note = next_note(self.order)
            
            states = update_states(states, new_note)
            
            piece.append(list(new_note))
            
            if leng > 20:
                break
            leng += 1
        
        return piece
    
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
                measures[i].append((leftover[0], leftover[1], leftover[2].denominator / leftover[2].numerator))
                count += leftover[2]
            
            count += note[2]
            
            if count > Fraction(top / bot):
                leftover = (note[0], note[1], count % 1)
                
                measures[i].append((note[0], note[1], (note[2] - leftover[2]).denominator / (note[2] - leftover[2]).numerator))
                count = 1
            else:
                measures[i].append((note[0], note[1], note[2].denominator / note[2].numerator))
                leftover = None
            
            count = count % 1
            
            if count == 0:
                i += 1
                            
        return measures
            
        
if __name__=="__main__":
    bot = ComposerBot("music/test.txt", "music/test2.txt")
    
    fp = open("piece.json", "w")
    
    json.dump(bot.measurify(bot.write(), 4, 4), fp)
    
    fp.close()