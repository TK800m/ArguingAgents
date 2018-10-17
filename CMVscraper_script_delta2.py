import time
import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import numpy as np

def souper(url):
    user_agent = 'Thijmen Kupers Student reseaching arguments on CMV: t.kupers@student.rug.nl'
    request = urllib.request.Request(url,headers={'User-Agent': user_agent})
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')
    return(soup)

def linksAndTopics(url):
    main_table = souper(url).find("div",attrs={'id':'siteTable'})
    comment_a_tags = main_table.find_all('a',attrs={'class':'bylink comments may-blank'})
    #Blank list to store the urls as they are extracted
    urls = [] 
    for a_tag in comment_a_tags:
        url = a_tag['href']
        if not url.startswith('http'):
            url = "https://reddit.com"+url
        urls.append(url)

    titles = main_table.find_all('a',attrs={'class':'title'})
    topics= []
    for topic in titles:
        t = topic.contents[0]
        topics.append(t)
    return(topics, urls)

def getOPtext(url):
    main_table = souper(url).find("div",attrs={'id':'siteTable'})
    OPtext = main_table.find("div", attrs={'class':'usertext-body'}).findAll('p')
    txt = ""
    for p in range(len(OPtext)):
        txt += OPtext[p].text

    OPwords = txt.split()


    OPname = main_table.find("a", attrs={'class':"author"})
    OPname = OPname.text
    
    return(txt, OPwords, OPname)

def getComments(url):
    deltabot = False
    comment_area = souper(url).find('div',attrs={'class':'commentarea'})
    comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
    extracted_comments = []
    textComm = []
    names = []
    delta_link = []
    for comment in comments: 
        if comment.find('form'):
            link = comment.find('a',attrs={'class':'bylink'})['href']
            commenter = comment.find('a',attrs={'class':'author'}).text
            comment_text = comment.find('div',attrs={'class':'md'}).text
            extracted_comments.append({'name':commenter,'text':comment_text})
            textComm.append(comment_text)
            names.append(commenter)
        if commenter == "DeltaBot":
            deltabot = True
            delta_link.append(link)
    return(extracted_comments, textComm, names, delta_link, deltabot)


def search(query):
    query = query.lower()
    TOPIC = None
    stop = False
    locURL = None
    deltabot = None
    url = "https://old.reddit.com/r/changemyview/"
    ##two vectors of topics and urls
    topics, urls = linksAndTopics(url)
    for i in range(len(topics)):
        splitTOP = topics[i].split()
        for x in range(len(splitTOP)):
            word = splitTOP[x].lower()
            if word == query:
                TOPIC = topics[i]
                #print(i)
                locURL = i
                stop = True
                break
    if stop == False:
        return(None,None,None,None,None,None,None, "No topic found")
    else:
        ##return all data
        URL = urls[locURL]
        OPtxt, OPwords, OPname = getOPtext(URL)
        comments, commentTXT, Names, deltalink, deltabot = getComments(URL)
        if deltabot == False:
            deltalink = None
        return(OPname, OPtxt, commentTXT, Names, URL, TOPIC, deltalink, deltabot)   
    
def urlSearch(query):
    url = "https://old.reddit.com/r/changemyview/"
    ##two vectors of topics and urls
    topics, urls = linksAndTopics(url)
    URL = urls[int(query)]
    ##return all data
    TOPIC = topics[int(query)]
    OPtxt, OPwords, OPname = getOPtext(URL)
    comments, commentTXT, Names, deltalink, deltabot = getComments(URL)
    return(OPname, OPtxt, commentTXT, Names, URL, TOPIC, deltalink, deltabot)  

#OPname, OPtxt, CommentText, commentName, URL, TOPIC, deltalink, deltabot= search("people")
#OPname, OPtxt, CommentText, commentName, URL, TOPIC, deltalink, deltabot= urlSearch("0")


def getDeltaNames(deltalink, deltabot, CommentText):
    if deltabot == True:
        deltaTXT = CommentText[0]
        deltaW = deltaTXT.split()
        deltaNumber = int(deltaTXT.split()[4])
        #print(deltaW)
        print(deltaNumber)
        print(deltalink[0])

    from bs4 import BeautifulSoup

    if deltalink != None:

        url = deltalink[0]
        store = []

        comment_area = souper(url).find('div',attrs={'class':'commentarea'})
        comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
        for comment in comments: 
                if comment.find('form'):
                    delta = comment.find('div', {'class': 'md'})
                    if delta.find('a', {'href': True}, text='here')!= None:
                        store.append(delta.find('a', {'href': True}, text='here'))

        deltaurl = str(store[0])
        #print(deltaurl)
        remove_letters = len(deltaurl)
        for i in range(len(deltaurl)):
            if deltaurl[i] == ">":
                remove_letters-=i - 1
                break

        #print(remove_letters)

        deltaurl = "https://old.reddit.com"+ deltaurl[9:-remove_letters]

        print(deltaurl)
        #print(store)

        store = []
        main_table = souper(deltaurl).find("div",attrs={'id':'siteTable'})
        entries = main_table.find_all("div",attrs={'class':'entry unvoted'})
        #print(main_table)
        #print(entries)
        for entry in entries:
            if entry.find('form'):
                #print(entry.find('form'))
                delta = entry.find('div', {'class': 'md'})
                #print(delta)
                allNames = delta.find_all('a', {'href': True})

        deltanames = []
        deltacomment = []
        for i in range(4,4+deltaNumber*2,2):
            print(i)
            deltanames.append(allNames[i].text)
            deltacomment.append(allNames[i+1].text)

        print(deltanames)
        print(deltacomment)
        return(deltanames, deltacomment)

		
#deltaNames, deltaComments = getDeltaNames(deltalink)
