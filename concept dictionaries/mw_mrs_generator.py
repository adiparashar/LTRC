from wxconv import WXC
import sys
import re
import os,subprocess

con = WXC(order='utf2wx')
def get_sentence(word,pos):
    if pos == 'verb' :
        return 'Please {}.'.format(word)
    elif pos == 'adj' :
        return 'This is {}.'.format(word)
    elif pos == 'noun' :
        return 'This is the {}.'.format(word)
    if pos == 'adv': 
        return 'He wants to do it {}.'.format(word)
    else:
        return word
f = open("mw-sansdict-v2.txt", 'r')
fr = f.readlines()
fw = open('amw-sans-eng-mrs_v1_dict.txt', 'w')
fw.write('Sans_Label'+'\t'+'Eng_Label'+'\t''POS' + '\t' +'MRS_Concept' +'\t'+'MRS_Feature_Values\n')

for i in range(1,len(fr)):
    try:
        lst = fr[i].split('\t')
        hinwrd = lst[1]
        engwrd = lst[2]
        word = engwrd
        cat = lst[3]
        pos = cat.strip('\n')
        fws = open('ace_input','w')
        engSent = get_sentence(word,pos)
        fws.write(engSent)
        fws.close()
        runACE_Command = ["./ace", "-g","erg-2018-osx-0.9.31.dat","-1Tf","ace_input"]
        result = subprocess.run(runACE_Command, stdout=subprocess.PIPE)
        aceOut = str(result.stdout,'utf-8')
        relstr = aceOut.split('RELS: <')[1]
        rels = relstr.split(' >')[0]
        finalRels = rels.split('\n')
        indx = engSent.find(word)
        splitter = '<' + str(indx) + ':' + str(len(engSent)) + '>'
        for r in finalRels: 
            concept = r.split(splitter)[0].split(' [ ')[1]

            if splitter in r : #and concept not in ignorelst:
                pat =  r'\[.*?\]' 
                featVal = r.split(splitter)[1]
                featureVals = re.sub(pat,'',featVal[:-1])
                if ' CARG: ' in featVal:
                    myentry = hinwrd + '\t' + engwrd + '\t' + cat.strip('\n') + '\t' + concept + '\t'+',CARG:_VALUES'
                    fw.write(myentry)
                    fw.write('\n')
                else:
                    featValLst = featureVals.split()
                    myFeatureValues = ''

                    for fv in range(len(featValLst)):
                        if fv%2 == 1:
                            myFeatureValues = myFeatureValues + featValLst[fv][0] + '* '
                        else:
                            myFeatureValues = myFeatureValues + featValLst[fv] + ' '
                    myentry = hinwrd + '\t' + engwrd + '\t' + cat.strip('\n') + '\t' + concept + '\t' + myFeatureValues
                    fw.write(myentry)
                    fw.write('\n')
    except:
        myentry = engwrd.strip() + ',SOME PROBLEM IN FATCHING MRS VALUES #############\n'
        fw.write("Oops!" + str(sys.exc_info()[0])+ "occurred.")
        fw.write(myentry)
        fw.write('\n')


fw.close()

