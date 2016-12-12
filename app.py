from flask import Flask, render_template, request, redirect
import subprocess
import sqlite3
import os.path
import time
import sys
import nltk
import ast
from DatabaseReader import DatabaseReader
from bson.objectid import ObjectId
from nltk.stem.wordnet import WordNetLemmatizer # princeton
lmtzr = WordNetLemmatizer()


if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf8')

#sys.path.append('/home/lpxz/deepLearning/translate-en2ch')
#import translateWrapper # takes long time at initialization

import word2veclib # takes long time at initialization

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

#posts = [("post1", "this is the first post HUrray fjawo;eij"), ("post2", "a;sodifjawo;eifja;woeifjaw;oeifjas;ldkfjha;skdjfhalskdjfhalskdjfhaskldjf")]

posts = [("qwerty","post1", "this is the first post HUrray fjawo;eij", [("Genji Noguchi","aowiejfoawiejfoiwaefoiawejfo"),("Swagmaster", "I am made of swag.")]), ("1a2bc3f","post2", "a;sodifjawo;eifja;woeifjaw;oeifjas;ldkfjha;skdjfhalskdjfhalskdjfhaskldjf",[("Super commenter","Comment 1"),("Even bigger commenter than ^","Massive comment")])]

#Must Run Commit After Function is called
def addPost (postdata, txtpostdata, time, curs):
    sinsertion = "INSERT INTO posts (title, post, time) values (" + "'" + str(postdata) +  "', '" + txtpostdata + "', " + str(time) + ");"
    curs.execute(sinsertion)

def addComment (postdata, username, time, pID, curs):
    sinsertion = "INSERT INTO comments (comment, username, time, pId) values (" + "'" + postdata +  "', '" + username + "', " + str(time) + ", '" + str(pID) + "');"
    print sinsertion
    curs.execute(sinsertion)

def getPosts (curs):
  result = curs.execute('SELECT * FROM posts')
  for row in result:
    print row
  return result

def getComms (curs):
  result = curs.execute('SELECT * FROM comments')
  print result
  for row in result:
    print row
  return result

def trending(a):
    one = 0
    oneCount = 0
    two = 0
    twoCount = 0
    three = 0
    threeCount = 0
    for post in a:
        count = 0
        for time in post:
            if time - time.time() <= 86400:
                count += 1
        if count > oneCount:
            three = two
            threeCount = twoCount
            two = one
            twoCount = oneCount
            one = post[0]
            oneCount = count
        elif count >= twoCount:
            three = two
            threeCount = twoCount
            two = post[0]
            twoCount = count
        elif count >= threeCount:
            three = post[0]
            threeCount = count
    return [one,two,three]


@app.route("/")
def index():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("index.html")

# top level categories    
@app.route("/nlp")
def nlp():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("nlp.html")

@app.route("/mobile")
def mobile():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("mobile.html")

@app.route("/bigdata")
def bigdata():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("bigdata.html")

@app.route("/security")
def security():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("security.html")

@app.route("/robot")
def robot():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("robot.html")

@app.route("/deeplearning")
def deeplearning():
    #Insert code here to fetch the trending posts now. -genji
    return render_template("deeplearning.html")

@app.route("/displaycode", methods= ['GET', 'POST'])
def displaycode(post_id=None):
    #INSERT CODE HERE TO ADD A NEW COMMENT TO THE POST -genji
    lines = []
#    if request.method == 'GET':
#        codeinfo = request.args.get('codeinfo')
#        print codeinfo 
    startLine = -1
    endLine = -1
    if request.method == 'POST':
        codeinfostr = request.form['codeinfo']
#{u'start': 357, u'end': 396, u'file': u'/Users/liup/Master/MaterialsInspect/Authentication/AuthenticationController.swift', u'funcname': u'loginViewController'}
        codeinfodict = ast.literal_eval(codeinfostr)    
        startLine =  int(codeinfodict['start'])
        endLine = int(codeinfodict['end']) 
        filename = codeinfodict['file']
        funcname = codeinfodict['funcname']
        if ".." not in filename and filename.endswith(".swift"):
            lines = [line.rstrip('\n') for line in open(filename)] 
#        for line in lines:
#            print line
    return render_template("code.html", mytitle="Code" , lines=lines, startLine=startLine, endLine=endLine)



# Category: nlpbase
@app.route("/word2vec", methods= ['GET', 'POST'])
def word2vec(post_id=None):
    #INSERT CODE HERE TO ADD A NEW COMMENT TO THE POST -genji
    findResults = {} 
    checkResult = "" 
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Find':
            word = str(request.form['word']).lower()
            similarResults = word2veclib.model.most_similar(word)
            for item in similarResults:
               findResults[item[0]]= item[1]
        elif cmd == 'Check': 
            word1 = str(request.form['word1']).lower()
            word2 = str(request.form['word2']).lower()
            similarity = word2veclib.model.similarity(word1, word2)
            checkResult = "similarity:"+ str(similarity)
    return render_template("word2vec.html", mytitle="Word2Vec" , findResults=findResults, checkResult= checkResult)


@app.route("/translation", methods= ['GET', 'POST'])
def translation(post_id=None):
    #INSERT CODE HERE TO ADD A NEW COMMENT TO THE POST -genji
    result = ""
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Translate':
            sentence = str(request.form['sentence']).lower()
            result = translateWrapper.translate(sentence)
            print result
    return render_template("translation.html", mytitle="Translation" , result=result )

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

@app.route("/verbnoun", methods= ['GET', 'POST'])
def verbnoun(post_id=None):
    #INSERT CODE HERE TO ADD A NEW COMMENT TO THE POST -genji
    verbs = {}
    nouns = {}
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Extract':
            sentence = str(request.form['sentence']).lower()
            pair = significantVerbsNouns(sentence)
            verbs = pair[0]
            nouns = pair[1]
    return render_template("verbnoun.html", mytitle="Extract Verbs and Nouns" , verbs=verbs, nouns=nouns)

def parsetree(phrase):
    phrase = phrase.replace('\'s', ' ').replace('\'', ' ')
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

@app.route("/syntaxparsetree", methods= ['GET', 'POST'])
def syntaxparsetree(post_id=None):
    #INSERT CODE HERE TO ADD A NEW COMMENT TO THE POST -genji
    tree = ""
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Parse':
            sentence = str(request.form['sentence']).lower()
            tree = parsetree(sentence) 
    return render_template("syntaxparsetree.html", mytitle="Syntax Parse Tree" , tree=tree)

from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
noisyThreshold = 0.3

def verbsNLTK(sentence):
    tokens = nltk.word_tokenize(sentence)
    text = nltk.Text(tokens)
    tags = nltk.pos_tag(text)
    verbs = [word for word,tag in tags if 'VB' in tag]
    return verbs

def nounsNLTK(sentence):
    tokens = nltk.word_tokenize(sentence)
    text = nltk.Text(tokens)
    tags = nltk.pos_tag(text)
    nouns = [word for word,tag in tags if 'NN' in tag]
    return nouns 

def phraseSimilarityFunc( sentence1, sentence2):
    total = 0.0
    set1 = sentence1.split() 
    set2 = sentence2.split()
    verbs1 = verbsNLTK(sentence1) # faster than syntaxnet
    verbs2 = verbsNLTK(sentence2) 
    for item1 in set1:
        if item1 in stop:
            continue
        if item1 in verbs1:
            item1= lmtzr.lemmatize(item1, 'v')
        else:
            item1= lmtzr.lemmatize(item1)
        similarity = 0.0
        for item2 in set2:
            if item2 in stop:
                continue
            if item2 in verbs2:
                item2= lmtzr.lemmatize(item2, 'v')
            else:
                item2= lmtzr.lemmatize(item2)

            localSimilarity = word2veclib.model.similarity(item1, item2)
            if localSimilarity > similarity:
                similarity = localSimilarity
        if similarity > noisyThreshold: # otherwise, we have to ignore the similarity by chance.
            total += similarity
    return total 




@app.route("/phrasesimilarity", methods= ['GET', 'POST'])
def phrasesimilarity(post_id=None):
    result =""
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Compute':
            sentence1 = str(request.form['sentence1']).lower()
            sentence2 = str(request.form['sentence2']).lower()
            similarity = phraseSimilarityFunc(sentence1, sentence2)
            result="similarity score: " + str(similarity)
    return render_template("phrasesimilarity.html", mytitle="Phrase Similarity" ,result=result) 
#
#

# Category: mobile research
#
#
#
#

# Category: mobile research
#

# Category: mobile research
#

# Category: mobile research

@app.route("/searchscreen", methods= ['GET', 'POST'])
def searchscreen(post_id=None):
    cur = []
    screenInput = ""
    topK = 3
    results = []
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Search':
            screenInput = str(request.form['screen']).lower()
            sentenceSub = regex.sub('', screenInput)
            if 'topK' in request.form and request.form['topK']:
               print "topK: ", request.form['topK']
               topK = int(str(request.form['topK']))
            print "finding topK for sentence", sentenceSub, topK
            reader = DatabaseReader()
            allscreens = reader.getAllScreens()
            cur = allscreens.find({})
            topKMatches = {}
            
            cache = {}
            for x in cur:
                HumanIntentions = reader.getHumanIntentions(x)
                if len(HumanIntentions) == 0:
                    continue
            
                HISub = regex.sub('', HumanIntentions[-1])
                if HISub not in cache:
                    sim = phraseSimilarityFunc(sentenceSub , HISub)
                    cache[HISub] = sim
                else:
                    sim = cache[HISub]

                if len(topKMatches) >= topK:
                    minItem = min(topKMatches, key=topKMatches.get)
                    if sim > topKMatches[minItem]:
                        del topKMatches[minItem]
                        topKMatches[x['_id']] = sim
                    else:
                        pass
                else:
                    topKMatches[x['_id']] = sim

            resultIDs = sorted(topKMatches, key=topKMatches.get, reverse=True)
            
            print "Final result:"
            for w in resultIDs:
                screen = allscreens.find_one({'_id':ObjectId(w)})
                results.append(screen)
                print screen, topKMatches[w]
    return render_template("searchscreen.html", mytitle="Search For Screen" ,result=results) 

import re
regex = re.compile('[^a-zA-Z ]')

def normalize(str):
    return regex.sub('', str.lower())


@app.route("/searchbutton", methods= ['GET', 'POST'])
def searchbutton(post_id=None):
# matching is based on two criteria: (1 ) screen description matching (2) button description matching
    cur = []
    screenInput = ""
    buttonInput = ""
    topK = 3
    results = []
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Search':
            if request.form['screen']:
                screenInput = normalize(str(request.form['screen']).lower())
            if request.form['button']:
                buttonInput = normalize(str(request.form['button']).lower())
            if request.form['topK']:
               topK = int(str(request.form['topK']))
            print screenInput, buttonInput, topK 

            reader = DatabaseReader()
            allbuttons = reader.getAllButtons()
            cur = allbuttons.find({})
            topKMatches = {}
            
            for x in cur:
                simScreen = 0
                simButton = 0
                if screenInput:
                    HumanIntentions = reader.getHumanIntentionsOfScreen(x)
                    if len(HumanIntentions) != 0:
                        HISub = normalize(HumanIntentions[-1])
                        simScreen = phraseSimilarityFunc(screenInput, HISub)
                        print "simScreen:", screenInput, HISub, simScreen
                if buttonInput:
                    buttonLabel = reader.getButtonLabel(x)
                    if buttonLabel:
                        buttonLabel = normalize(buttonLabel)
                        simButton = phraseSimilarityFunc(buttonInput, buttonLabel)
                        print "simButton", buttonInput, buttonLabel, simButton
                simTotal = simScreen + simButton
                if len(topKMatches) >= topK:
                    minItem = min(topKMatches, key=topKMatches.get)
                    if simTotal > topKMatches[minItem]:
                        del topKMatches[minItem]
                        topKMatches[x['_id']] = simTotal 
                    else:
                        pass
                else:
                    topKMatches[x['_id']] = simTotal 

            resultIDs = sorted(topKMatches, key=topKMatches.get, reverse=True)
            
            print "Final result:"
            for w in resultIDs:
                button = allbuttons.find_one({'_id':ObjectId(w)})
                results.append(button)
                print button, topKMatches[w]
                

    return render_template("searchbutton.html", mytitle="Search For Button" ,result=results) 


@app.route("/showallscreens", methods= ['GET', 'POST'])
def showallscreens(post_id=None):
    cur = []
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Show':
            reader = DatabaseReader()
            allscreens= reader.getAllScreens()
            cur = allscreens.find({})
    return render_template("showallscreens.html", mytitle="Show All Screens" ,result=cur) 


@app.route("/showallbuttons", methods= ['GET', 'POST'])
def showallbuttons(post_id=None):
    cur = []
    if request.method=='POST':
        cmd = str(request.form['command'])
        if cmd == 'Show':
            reader = DatabaseReader()
            allbuttons = reader.getAllButtons()
            cur = allbuttons.find({})

    return render_template("showallbuttons.html", mytitle="Show All Buttons" ,result=cur) 








if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=33333)
