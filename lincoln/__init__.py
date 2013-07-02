import nltk
import os
import markov
import random

# history:
    # first order markov model
    # teach gramar with first order markov model
    # nltk and first order but distinguish word type
    # second order nltk
    # nth order nltk

# parse part of speech for lincoln texts
    # parse sentence structure for lincoln texts
        # parse paragraph structure

# write speech:
    # for length of speech, create paragraph length
        # for length of paragraph, create sentence:
            # decide sentence structure
                # decide words based on structure
class LincolnBot:

    def __init__(self, files, order):
        self.train(files,order)

    def train(self, files, order):
        self.order = order
        self.chains = []
        
        for file in files:
            fp = open(os.getcwd() + "/" + file, "r")
            
            speech = fp.read()
            
            sentences = nltk.sent_tokenize(speech)
            
            for i in range(0, self.order):
                try:
                    self.chains[i]
                except:
                    self.chains.append(markov.MarkovChain())
            
            for sentence in sentences:
                tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
                
                for i in range(1, self.order+1):
                    self.add_to_markov_chain(self.chains[i-1], tagged, i)
          
            fp.close()
    
    def add_to_markov_chain(self, chain, sentence, order):
        
        if order > len(sentence):
            order = len(sentence)
        
        for i in range(0, len(sentence) - (order + 1)):
            words = []
            parts = []
            
            for j in range(0, order):
                words.append(sentence[i+j][0].lower())
                
                parts.append(sentence[i+j][1])
            
            next_word = sentence[i+order][0].lower()
            next_part = sentence[i+order][1]
            
            key = []
            
            for k in range(0,len(words)):
                key.append((words[k],parts[k]))
            
            key = tuple(key)

            try:
                chain[key]
            except KeyError:
                chain[key] = State()
            
            chain[key].add_side((next_word,next_part))
        return chain
    
    def write_sentence(self):
        def set_rand_states():
            states = []
            
            starts = ("IN", "PDT", "NNP", "NNPS", "RB")
            
            rand_state = random.choice([key for key in self.chains[self.order - 1].keys() if key[0][1] in starts])
            temp = self.chains[self.order-1].set_current_state(rand_state)

            for i in range(1, self.order):
                states.append(self.chains[i-1].set_current_state(temp[self.order-i:]))
            states.append(temp)
            
            return states
        
        def update_states(states, latest_word):
            new_states = []
            
            # update array
            for state in states:
                new_state = []
                
                for i in range(1,len(state)):
                    new_state.append(state[i])
                
                new_state.append(latest_word)
                
                new_states.append(tuple(new_state))
            
            # update markov chain
            for i in range(0, self.order):
                self.chains[i].set_current_state(new_states[i])
            
            return new_states
        
        def next_word(order):
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
                    

                return next_word(order)
        
        
        states = set_rand_states()
        sentence = ""
        
        # create beginning of sentence
        for word in states[len(states) -1]:
            sentence += " " + word[0]
        sentence = sentence[1:]
            
        ends = ("VBD")
        bad_ends = ("have", "be", "was", "were")
        punctuation = (";", ",", ":")
        #, "VBD", "VBN", "VBP", "VBZ")
        
        while True:
            new_word = next_word(self.order)
            
            states = update_states(states, new_word)
            
            if new_word[1] in punctuation:
                sentence += new_word[0]
            else:
                sentence += " " + new_word[0]
            
            if len(sentence.split()) > 15 and (new_word[1] in ends) and (new_word[0] not in bad_ends):
                break
        
        return sentence + "."