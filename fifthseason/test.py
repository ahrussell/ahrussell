import suffix_tree
import music_notes

class Pattern():
    def __init__(self, rel_pitch, rhythm, baselines):
        self.rel_pitch = rel_pitch # list of relative pitches (ie [-2,2,3] etc)
        self.rhythm = rhythm # list of rhythms (ie [1/4, 1/2, 3/4])
        self.baselines = baselines # dict ie {(G, 1/8): [1,3]} the list is the positions of the ends of the baseline for markov extraction

music = music_notes.MusicSequence("music/test.txt")

stri2 = music.to_string().replace(" ", "")
stri = music.to_relative_string().replace(" ", "")
stri += "$"

stree = suffix_tree.SuffixTree(stri)

p = stree.get_patterns1(2)

print "-"*60
print stri
print "-"*60
print

comps = {}

for x in p:
    try:
        comps[stri[x[0]:x[1]+x[0]]] +=1
    except KeyError:
        comps[stri[x[0]:x[1]+x[0]]] = 1

for key,comp in comps.iteritems():
    print key+ ": " + str(comp)
    print

'''for x in p:
    s = ""
    print stri2[x[0]:x[1]+x[0]]
    for c in stri[x[0]:x[1]+x[0]]:
        s += str(ord(c) - 75)
    print s
    #print stri[x[0]:x[1]+x[0]] + " " + stri[x[0]+x[1]]'''

'''for x in p:
    
    s = ""
    for c in stri[x[0]:x[1]+x[0]]:
        s += c #str(ord(c) - 75) + " "
    print s
    print x
    
    print'''

#print stree

'''for x,edge in stree.edges.iteritems():
    print stri[edge.first_char_index:edge.last_char_index+1]
    print edge.depth'''

'''for x in range(len(stree.nodes)):
    print x
    print stree.nodes[x].depth'''