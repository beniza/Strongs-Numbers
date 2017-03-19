import xml.etree.ElementTree as ET
import pdb, codecs
import lexicon, Scripture

kjvDict={}
knum = 1
def getKJVnum(s):
    global knum
    try:
        kjvDict[s][1] += 1
        return(kjvDict[s][0])
    except:
        kjvDict[s]=["KJV"+str(knum).zfill(5), 1]
        knum += 1 
        return(kjvDict[s][0])

tree = ET.parse('kjv_plus.xml')
root = tree.getroot()

bk = ""
ch = ""
vn = ""
strong = ""
vt_e = ""
vt_sn = ""
sn=[]
cnt=0
gr = ""
tr = ""
gl = ""
mp = ""
pre= "" #To add the H or G prefix before Hebrew and Greek numbers

o = codecs.open("kjv.tab", mode='w', encoding='utf-8')
for b in root.iter('BIBLEBOOK'):
    bk = b.attrib['bnumber']

    # Adding the Hebrew and Greek prefix
    if(int(bk)<40):
        pre="H"
    else:
        pre="G"

    bk = Scripture.getBookCode(bk)
    print("processing " + bk)
    for c in b:
        ch= c.attrib['cnumber']
        for v in c:
            # if(cnt <5 and b.attrib['bnumber']=="3"):
            vn  = v.attrib['vnumber']
            cnt += 1
            for g in v.iter():
                if(g.tag=="VERS" and g.text):
                    kjvnum=getKJVnum(g.text.strip("\n"))
                    sn.append((kjvnum, g.text.strip("\n"),))
                if(g.tag == 'gr'):
                    t = ""
                    if(g.text):
                        t=g.text
                    sn.append((pre+str(g.attrib['str']), t))
                    lx = lexicon.getLexicon(pre+str(g.attrib['str']))
                    if(g.tail):
                        if(g.tail != "\n"):
                            kjvnum=getKJVnum(g.tail.strip("\n"))
                            sn.append((kjvnum, g.tail.strip("\n"),))
                elif(g.tail):
                    # if(g.tail!="\n"):
                    sn.append(g.tail.strip("\n"))
                # vt_sn = "\n%s\t%s\t%s\t%s\t" % (str(cnt), bk, ch, vn,)
                # vt_sn = vt_e
                for item in sn:
                    if(isinstance(item,tuple)):
                        vt_sn = "\n%s\t%s\t%s\t" % (bk, ch, vn,)
                        vt_sn += str(item[0])+ "\t"
                        vt_sn += str(item[1]) + "\t"
                        # pdb.set_trace()
                        o.write(vt_sn) # + vt_e) # + vt_gr + vt_tr + vt_gl + vt_mp + "\n")
                sn = []
o.close()
