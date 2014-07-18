from textblob import TextBlob
import time
import io
import os
import urllib 
import pickledb
import json 
import requests
from pprint import pprint
from textblob import TextBlob 
import chartFunctions
import random

from peewee import *
DATABASE = {
    'name': 'data/db.db',
    'engine': 'peewee.SqliteDatabase',
}


db = SqliteDatabase('data/db.db')

class Product(Model):
    link = CharField()
    name = CharField()
    price = CharField()
    pic = CharField()
    posCount = IntegerField()
    negCount = IntegerField()
    neutCount = IntegerField()

    class Meta:
        database = db # this model uses the people database

class Comment(Model):
    productLink = ForeignKeyField(Product, related_name='links')
    comment = TextField()  

    class Meta:
        database = db # this model uses the people database



def grabkimono(products): 
   #products = ["http://www.amazon.com/Apple-MD199LL-A-TV/dp/B007I5JT4S", "http://www.amazon.com/Google-Chromecast-Streaming-Media-Player/dp/B00DR0PDNE"]  for s in products:
    for s in products:
        productName = s.split("/")[3] 
        idOfProduct = s.split("/")[5] 
        grabNoOfPages = 10     
        counter = 1
        for x in range(1,grabNoOfPages+1):
            api = "https://www.kimonolabs.com/api/b6mvxgxs?apikey=68d2fb6d1d7f5448161a279564ed03fc" +"&kimpath1=" + productName + "&kimpath2=" + "product-reviews" + "&kimpath3=" + idOfProduct + "&kimpath4=" + "ref=cm_cr_pr_top_link_"+ str(x) + "&pageNumber="+ str(x)
            print api

            time.sleep(1) # delays for 5 seconds
            results =""
            print results 
         
            r = requests.get(api)
            with open("data/"  + str(counter) + productName +  ".txt", 'wb') as fd:
                for chunk in r.iter_content(10):
                    fd.write(chunk)
            counter +=1


def read(f): 
    with open(f) as data_file:    
        data = json.load(data_file)
        #pprint(data)
        return data



def isbogus(mystring):
    if len(mystring.split()) < 3:
        #print "++++++++++bogus: " + mystring
        return True
    bogusSentences = ["This review is from:", "PermalinkComment","Was this review helpful to you"]
    for x in bogusSentences:
        if x in mystring:
            #print "++++++++++bogus: " + mystring
            return True 
    #print  mystring
    return False 

def kimonoComments2DB(p,grabNoOfPages): 
   #products = ["http://www.amazon.com/Apple-MD199LL-A-TV/dp/B007I5JT4S", "http://www.amazon.com/Google-Chromecast-Streaming-Media-Player/dp/B00DR0PDNE"]  for s in products:


    productName = p.link.split("/")[3] 
    idOfProduct = p.link.split("/")[5]   
    for x in range(1,grabNoOfPages+1):
        api = "https://www.kimonolabs.com/api/b6mvxgxs?apikey=68d2fb6d1d7f5448161a279564ed03fc" +"&kimpath1=" + productName + "&kimpath2=" + "product-reviews" + "&kimpath3=" + idOfProduct + "&kimpath4=" + "ref=cm_cr_pr_top_link_"+ str(x) + "&pageNumber="+ str(x)
        print api

        time.sleep(2) # delays for 5 seconds
        results =""
        print results 
     
        r = requests.get(api)
        with open("tmp.txt", 'wb') as fd:
            for chunk in r.iter_content(10):
                fd.write(chunk) 

        fpath = "tmp.txt"
        f = read(fpath) 

        os.remove(fpath)

       # data = [{"price": 1, "name": "xxx", "comments" : commentList}]
        try: 
            for comment in f['results']['collection1']: 
                txt =""
                try: 
                    txt = comment['property1']['text'].strip()
                except:
                    txt = comment['property1'].strip()

                if(isbogus(txt)):
                    continue 

                try: 
                    c = Comment(productLink = p, comment = txt)
                    c.save()
                except:
                    print "double"
                #price = comment['property1']['price'].strip()
                #pic = comment['property1']['pic'].strip()
                #name = comment['property1']['name'].strip()
        except: 
            print "for loop failed"



def parseFiles(pLink,grabNoOfPages):        

    pName = pLink.split("/")[3] 

    ssum = 0.0
    psum = 0.0
    total = 0.0
    for counter in range(1,grabNoOfPages+1):

        fpath = "data/products/" + str(counter) + pName + ".txt"
        f = read(fpath) 

        for comment in f['results']['collection1']: 
            txt =""
            try: 
                txt = comment['property1']['text'].strip()
            except:
                txt = comment['property1'].strip()

            if(isbogus(txt)):
                continue

            pprint(txt)
            txtBlob = TextBlob(txt)
            p = float(txtBlob.sentiment.polarity)
            s = float(txtBlob.sentiment.subjectivity)
            #print str(p)  +  " "   + str(s)
            ssum += s
            psum += p
            total += 1.0

    print "total avg polar: " + str(psum/total)
    print "total avg subj: " + str(ssum/total)
    print "total comments: " + str(total)

def parseFilesSentences(pLink,grabNoOfComments):
    pName = pLink.split("/")[3] 
    ssum = 0.0
    psum = 0.0
    total = 0.0

    posBin = 0
    neutBin = 0
    negBin = 0 

    res = []
    res.append(pName)

    for counter in range(1,grabNoOfPages+1):

        fpath = "data/products/" + str(counter) + pName + ".txt"
        f = read(fpath) 

        for comment in f['results']['collection1']: 
            txt =""
            try: 
                txt = comment['property1']['text'].strip()
            except:
                txt = comment['property1'].strip()

            if(isbogus(txt)):
                continue
                
            #pprint(txt)
            txtBlob = TextBlob(txt)
            for sentence in txtBlob.sentences: 
                p = float(sentence.sentiment.polarity)
                s = float(sentence.sentiment.subjectivity)
                #print str(p)  +  " "   + str(s)
                ssum += s
                psum += p
                total += 1.0

                if p == 0.0:
                    neutBin += 1.0
                elif p < 0.0:
                    negBin += 1.0
                else:
                    posBin += 1.0

    print "total avg polar: " + str(psum/total)
    print "total avg subj: " + str(ssum/total)
    print "total comments: " + str(total) 
    print "total posbin: " + str(posBin)
    print "total negbin: " + str(negBin)
    print "total neutbin: " + str(neutBin)
    res.append(posBin)
    res.append(negBin)
    res.append(neutBin)
    return res

def parseProductBySentencesSaveVibes(p,grabNoOfComments):
    pName = p.name
 

    ssum = 0.0  

    posBin = 0
    neutBin = 0
    negBin = 0 

    counter = 0
    for c in Comment.select().where(Comment.productLink == p):
        txt = c.comment
        txtBlob = TextBlob(txt)
        for sentenceLine in txtBlob.sentences: 
            vibe = float(sentenceLine.sentiment.polarity)
            subj = float(sentenceLine.sentiment.subjectivity)
            #print str(p)  +  " "   + str(s)
            ssum += subj
            #psum += p
            #total += 1.0

            if vibe == 0.0:
                neutBin += 1.0
            elif p < 0.0:
                negBin += 1.0
            else:
                posBin += 1.0

            sent = Sentence(productLink=p, comment = c, vibe = vibe, subjectivity = subj, length = len(sentenceLine))
            sent.save()

        counter += 1
        #if (counter  == grabNoOfComments):
        #    break
    v = Vibe(productLink=p, posCount=posBin,  negCount=negBin,  neutCount=neutBin, subjectivity = (ssum/(posBin + negBin + neutBin)))
    v.save() 

    print "total avg polar: " + str(psum/total)
    print "total avg subj: " + str(ssum/total)
    print "total comments: " + str(total) 
    print "total posbin: " + str(posBin)
    print "total negbin: " + str(negBin)
    print "total neutbin: " + str(neutBin) 

def compareAndPrint(p1,p2,pNo1,pNo2): 
    s1=parseFilesSentences(p1,pNo1)
    total1 = s1[1] + s1[2] + s1[3] 

    s2=parseFilesSentences(p2,pNo2) 
    total2 = s2[1] + s2[2] + s2[3] 

    #nachjustieren
    diff = (total1 - total2)
    if abs(diff) > 30:
        s2 = parseFilesSentences(p2,pNo2 + int(diff/70))
        print "nachjustierung: " + str(int(diff/70))

    #html = chartFunctions.getHTMLFromDataDonut(s1,s2)
    #html = "<br>"
    html = chartFunctions.getHTMLFromDataBarChart(s1,s2)
    f = open("data/charts/" + str(pNo1) + "to" + str(pNo2) + p1.split("/")[3] + '-vs.-' + p2.split("/")[3] + '-chart.html','w')
    f.write(html) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if
    print "+++++++++++DONE+++++++++++++++++++++"
    return html

def top100Json2List(fpath): 
    f = read(fpath)  

    # data = [{"price": 1, "name": "xxx", "comments" : commentList}]
    commentList = []
    for comment in f['results']['twenty']:  
        #print comment
        name = comment['title']['text'].strip()
        txt = comment['title']['href'].strip()
        txt = txt.split("\n\n\n\n\n\n\n")[1]  
        price = comment['price']
        pic ="" 
        try:
            pic = comment['pic']['src']
        except:
            print "ups" 
        
        p = Product(link=txt, name=name, pic=pic, price=price, posCount = 0, negCount = 0, neutCount = 0)
        p.save()

#kimonoComments2PickleDB([top100Json2List("data/kimonoData.json")[0]],1)

#top100Json2List("data/kimonoData.json")
#for p in Product.select():
 #   kimonoComments2DB(p,10)

for p in Product.select():
    parseProductBySentencesSaveVibes(p,-1000)

def goParse100():
    tmp = parseTop100Files("data/kimonoData.json")
    res = []
    #print len(tmp) 
    #r1 =  tmp[random.randint(1, len(tmp))]
    #r2 =  tmp[random.randint(1, len(tmp))]
     
    for x in tmp:
        #print x
        res.append(x)
    return res

p = ["http://www.amazon.com/Google-Chromecast-Streaming-Media-Player/dp/B00DR0PDNE/ref=zg_bs_electronics_1/184-6199652-9954344","http://www.amazon.com/Roku-3-Streaming-Media-Player/dp/B00BGGDVOO/ref=zg_bs_electronics_7/184-6199652-9954344"]

#grabkimono(p)

#compareAndPrint(p[0],p[1],10,10)

def jsonTop100ToRankAndUrl(): 
    l = parseTop100Files("data/top100_11.07.json") 
    with open("data/rankAndUrlTop100_11.07.json", 'w') as outfile:
        json.dump(l, outfile) 

def compareAll():
    for x, left in enumerate(res):
        print x
        print left

#parseTop100Files("data/top100_11.07.json") 
#jsonTop100ToRankAndUrl()
#products = ["http://www.amazon.com/Apple-MD788LL-Silver-NEWEST-VERSION/dp/B00G2Y4WNY/ref=sr_1_1?s=electronics&ie=UTF8&qid=1404912902&sr=1-1&keywords=ipad+air","http://www.amazon.com/Google-Nexus-10-Wi-Fi-only/dp/B00ACVI202/"]
#grabkimono()
#print len( parseTop100Files("data/top100_11.07.json")[0])
#play()
#parseFiles(pName,10)
#parseFilesSentences(pName,10)
#print read('data/1Apple-MD788LL-Silver-NEWEST-VERSION.txt')
#grabkimono()

#s1 = ["Apple Ipad version xy", 111,222,333]