import json
from pymongo import MongoClient
class DatabaseReader:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test
    def getAllButtons(self):
        allbuttons = self.db.buttonTable
        return allbuttons
    def getAllScreens(self):
        allScreens = self.db.screenTable
        return allScreens

#   the following is about the button
    def getHumanIntentionsOfScreen(self, jsonstr):
        return jsonstr["HumanIntentionsOfScreen"]

    def getUILabelsOfScreen(self,jsonstr):
        return jsonstr["UIlabelsOfScreen"]

    def getButtonLabel(self,jsonstr):
        return jsonstr["ButtonLabel"]

    def getCodeInfo(self,jsonstr):
        try:
            x = jsonstr["CodeInfo"]
            if type(x) is dict:
                return x
            else:
                return None
        except:
            return None
    def getCodeStart(self,jsontr):
        codeinfo = self.getCodeInfo(jsontr)
        if codeinfo is None:
            return None
        return codeinfo["start"]


    def getCodeEnd(self,jsonstr):
        codeinfo = self.getCodeInfo(jsonstr)
        if codeinfo is None:
            return None
        return codeinfo["end"]
    def getCodeFile(self,jsonstr):
        codeinfo = self.getCodeInfo(jsonstr)
        if codeinfo is None:
            return None
        return codeinfo["file"]
    def getCodeFuncname(self,jsonstr):
        codeinfo = self.getCodeInfo(jsonstr)
        if codeinfo is None:
            return None
        return codeinfo["funcname"]
# the following is about screen

    def getHumanIntentions(self, jsonstr):
        return jsonstr["HumanIntentions"]

#english = "Inspecting meeting"
#import re
#regex = re.compile('[^a-zA-Z ]')
#englishSub = regex.sub('', english)
#
#
#reader = DatabaseReader()
#allbuttons = reader.getAllButtons()
#cur = allbuttons.find({})
#
#maxSimilarity = 0
#max = None
#
#cache = {}
#
#
#for x in cur:
#    HumanIntentions = reader.getHumanIntentionsOfScreen(x)
#    if len(HumanIntentions) == 0:
#        continue
#
#    HISub = regex.sub('', HumanIntentions[-1])
#    if HISub not in cache:
#        sim = ss.phraseSimilarity(englishSub, HISub)
#        cache[HISub] = sim
#    else:
#        sim = cache[HISub]
#
#
#
#    if sim > maxSimilarity:
#        max = x



