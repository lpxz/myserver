import subprocess
import json
from requests import get
import argparse



sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2, type='relation', corpus='webbase'):
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return -1.0

def parsetree(phrase):
    phrase = phrase.replace('\'s', ' ').replace('\'', ' ')
    import os
    currentfolder = "/home/lpxz/deepLearning/tensorflowModels/syntaxnet"
    process = subprocess.Popen("echo "+ phrase + "|syntaxnet/demo.sh", cwd = currentfolder, shell=True, stdout=subprocess.PIPE)
    process.wait()

    tree = []
    startRecording = False
    for line in iter(process.stdout.readline,''):
        if line.startswith("Syntax Parse Tree!"):
            startRecording = False
            break

        if startRecording:
            tree.append(line)

        if line.startswith("Syntax Parse Tree:"):
            startRecording = True


    return tree



def significantVerbsNouns(phrase):
    # preprocess, because sh -c 'command', if command has ' inside, it is bad.
    phrase = phrase.replace('\'s', ' ').replace('\'', ' ')

    # note the cwd is correct only for the remote server.
    # if you want to use locally, cwd=/Users/liup/models/syntaxnet
    currentfolder = "/home/lpxz/deepLearning/tensorflowModels/syntaxnet"
    process = subprocess.Popen("echo "+ phrase + "|syntaxnet/demo.sh", cwd = currentfolder, shell=True, stdout=subprocess.PIPE)
    process.wait()
    verbs = {}
    nouns = {}

    for line in iter(process.stdout.readline,''):
        if line.startswith("significant verb"):
            seg = line.strip().split(":")[1]
            parts = seg.split(" ")
            verbs[parts[0]] = int(parts[1])

        if line.startswith("significant noun"):
            seg = line.strip().split(":")[1]
            parts = seg.split(" ")
            nouns[parts[0]] = int(parts[1])

    return [verbs, nouns]




def handle(urlAddr):
    from json import dumps
    from urlparse import parse_qs, urlparse
    import json
    queryDic = parse_qs(urlparse(urlAddr).query, keep_blank_values=True)
    if 'word2vec' in queryDic:
        import word2vec
        servicename = queryDic['word2vec'][0]
        if servicename == "similarity":
            input1 = queryDic['word1'][0]
            input2 = queryDic['word2'][0]
            similarity = word2vec.model.similarity(input1, input2)
            rv = {"similarity": similarity}
            return json.dumps(rv)
        elif servicename == "mostsimilar":
            input = queryDic['word'][0]
            similarResults = word2vec.model.most_similar(input)
            rv = {}
            for item in similarResults:
               rv[item[0]]= item[1]
            return json.dumps(rv) 
        else:
            pass

    elif 'syntaxnet' in queryDic:
        servicename = queryDic['syntaxnet'][0]
        sentence = queryDic['sentence'][0]
        if servicename.lower() == "verbnoun":
            pair = significantVerbsNouns(sentence)
            verbs = pair[0]
            nouns = pair[1]

            rv = {}
            rv["verbs"] = verbs
            rv["nouns"] = nouns

            return json.dumps(rv)
        elif servicename.lower() == 'parser':
            tree = parsetree(sentence)
            rv={"tree":tree}
            return json.dumps(rv)


        else:
            pass

    elif 'translate' in queryDic:
        import sys
        reload(sys)
        sys.path.append('/home/lpxz/deepLearning/translate-en2ch')
        import translateWrapper # takes long time at initialization
        sys.setdefaultencoding('utf-8')


        servicename = queryDic['translate'][0]
        sentence = queryDic['sentence'][0]
        if servicename.lower() == "en2ch":
            translation = translateWrapper.translate(sentence)
            rv = {"translation": translation}
            return json.dumps(rv, ensure_ascii=False, encoding='UTF8')
        else:
            pass
    elif 'phrase1' in queryDic and 'phrase2' in queryDic:
        phrase1 = queryDic['phrase1'][0]
        phrase2 = queryDic['phrase2'][0]
        ret = sss(phrase1, phrase2)
        rv = {"similarity": ret}
        return json.dumps(rv)
    else:
        rv={"hello":"world"}
        return json.dumps(rv)
        


import sys
if len(sys.argv) == 2:
     print handle(sys.argv[1])#.encode('UTF8')




#if __name__=='__main__':
#     x = handle("http://g.com/?word2vec=mostsimilar&word=cat")
#     print x
