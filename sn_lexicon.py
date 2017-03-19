import codecs
import re, pdb

f = codecs.open("NTStrongs.tab", mode='r', encoding="utf-8")

strongLexicon = f.readlines()
lexicon={}
for line in strongLexicon:
    e = line.split("\t")
    sn = e[3] # Strong's number
    gr = e[4] # Greek word form
    tr = e[5] # Transliterated text
    gl = e[6] # Gloss
    mrp = e[7].strip("\r") # Parsing info
    if(sn in lexicon):
        pass
    else:
        lexicon[sn]=[sn, gr, tr, gl, mrp]
o=codecs.open("lexicon.dict", mode="w", encoding="utf-8")
o.write(str(lexicon))
o.close()
