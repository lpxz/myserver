import subprocess
from bottle import route, response, run
import json
from requests import get
import word2vec # takes long time at initialization
import argparse
import sys
sys.path.append('/home/lpxz/deepLearning/translate-en2ch')
import translateWrapper # takes long time at initialization






parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-m','--mode', help='local or remote mode', default='remote')
args = vars(parser.parse_args())


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
    currentfolder = "/home/lpxz/deepLearning/tensorflowModels/syntaxnet"
    if args['mode'] == 'local':
        currentfolder = "/Users/liup/models/syntaxnet"
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
    if args['mode'] == 'local':
        currentfolder = "/Users/liup/models/syntaxnet"
    process = subprocess.Popen("echo "+ phrase + "|syntaxnet/demo.sh", cwd = currentfolder, shell=True, stdout=subprocess.PIPE)
    process.wait()
    verbs = {}
    nouns = {}

    for line in iter(process.stdout.readline,''):
        print line
        if line.startswith("significant verb"):
            seg = line.strip().split(":")[1]
            parts = seg.split(" ")
            print seg
            verbs[parts[0]] = int(parts[1])

        if line.startswith("significant noun"):
            seg = line.strip().split(":")[1]
            parts = seg.split(" ")
            print seg
            nouns[parts[0]] = int(parts[1])

    return [verbs, nouns]


#def translate(phrase):
#    phrase = phrase.replace('\'s', ' ').replace('\'', ' ')
#
#    # note the cwd is correct only for the remote server.
#    # if you want to use locally, cwd=/Users/liup/models/syntaxnet
#    currentfolder = "/home/lpxz/deepLearning/translate-en2ch"
#    process = subprocess.Popen("echo "+ phrase + "|python translate.py --decode", cwd = currentfolder, shell=True, stdout=subprocess.PIPE)
#    process.wait()
#    verbs = {}
#    nouns = {}
#
#    for line in iter(process.stdout.readline,''):
#        print line
#        if line.startswith(">"):
#            translation = line.strip().split(">")[1]
#            return translation.strip()
#
#    return "" 




@route("/")
def top():
    from bottle import response
    from json import dumps
    from bottle import request

    #
    queryDic = request.query.decode()

    if 'word2vec' in queryDic:

        servicename = queryDic['word2vec']
        if servicename == "similarity":
            input1 = queryDic['word1']
            input2 = queryDic['word2']
            similarity = word2vec.model.similarity(input1, input2)
            rv = {"similarity": similarity}
            response.content_type = 'application/json'
            return dumps(rv)
        elif servicename == "mostsimilar":
            input = queryDic['word']
            similarResults = word2vec.model.most_similar(input)
            rv = {}
            for item in similarResults:
               rv[item[0]]= item[1]
            response.content_type = 'application/json'
            return dumps(rv)
        else:
            pass

    elif 'syntaxnet' in queryDic:
        servicename = queryDic['syntaxnet']
        sentence = queryDic['sentence']
        if servicename.lower() == "verbnoun":
            pair = significantVerbsNouns(sentence)
            verbs = pair[0]
            nouns = pair[1]

            rv = {}
            rv["verbs"] = verbs
            rv["nouns"] = nouns

            response.content_type = 'application/json'
            return dumps(rv)
        elif servicename.lower() == 'parser':
            tree = parsetree(sentence)
            rv={"tree":tree}
            response.content_type = 'application/json'
            return dumps(rv)


        else:
            pass


    elif 'translate' in queryDic:
        servicename = queryDic['translate']
        sentence = queryDic['sentence']
        if servicename.lower() == "en2ch":
            translation = translateWrapper.translate(sentence)
            rv = {}
            rv["translation"] = translation 
            response.content_type = 'application/json'
            return dumps(rv)
        else:
            pass
    elif 'phrase1' in queryDic and 'phrase2' in queryDic:
        phrase1 = queryDic['phrase1']
        phrase2 = queryDic['phrase2']
        ret = sss(phrase1, phrase2)
        rv = {"similarity": ret}
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        rv={"hello":"world"}
        response.content_type = 'application/json'
        return dumps(rv)
        









# 0.0.0.0 is needed if you want to deploy it remotely. It means "for any computer".
if __name__ == "__main__":
    run(host="0.0.0.0", port=31415)
