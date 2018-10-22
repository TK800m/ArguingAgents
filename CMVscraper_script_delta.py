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
            url = "https://old.reddit.com"+url
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
            if len(names)>0:
                commenter = "u/unknown"                
            elif comment.find('a',attrs={'class':'author'}).text!= None:
                    commenter = comment.find('a',attrs={'class':'author'}).text
            else:
                commenter = "u/unknown"
            comment_text = comment.find('div',attrs={'class':'md'}).text
            extracted_comments.append({'name':commenter,'text':comment_text})
            textComm.append(comment_text)
            names.append(commenter)
        if len(names)>0 and names[0] == "DeltaBot":
            deltabot = True
            delta_link.append(link)
    return(extracted_comments, textComm, names, delta_link, deltabot)


def urlSearch(query):
    import math
    page_number = math.floor(query/25)
    item = query-(page_number*25)
    if item ==24:
        item -=1
    url =  "https://old.reddit.com/r/changemyview/"
    if page_number <1:
        url = url
    else:
        for i in range(page_number):
            url = get_next_page(url)
    ##two vectors of topics and urls
    topics, urls = linksAndTopics(url)
    
    URL = urls[item]
    ##return all data
    TOPIC = topics[item]
    OPtxt, OPwords, OPname = getOPtext(URL)
    comments, commentTXT, Names, deltalink, deltabot = getComments(URL)
    return(OPname, OPtxt, commentTXT, Names, URL, TOPIC, deltalink, deltabot)  

def get_next_page(url):
    url = souper(url).find_all("span",attrs={'class':"next-button"})
    url = str(url).split('>')[1].split("\"")[1]
    return url
    


#OPname, OPtxt, CommentText, commentName, URL, TOPIC, deltalink, deltabot= search("people")
#OPname, OPtxt, CommentText, commentName, URL, TOPIC, deltalink, deltabot= urlSearch("0")


def getDeltaNames(deltalink, deltabot, CommentText):
    if deltabot == True:
        deltaTXT = CommentText[0]
        deltaW = deltaTXT.split()
        deltaNumber = int(deltaTXT.split()[4])
        #print(deltaW)
        #print(deltaNumber)
        #print(deltalink[0])

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

        #print(deltaurl)
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
                comment_a_tags = delta.find_all('a',attrs={'href':True})
                delta_urls = []
                for a_tag in comment_a_tags:
                    delta_url = a_tag['href']
                    delta_urls.append(delta_url)
        #print(delta_urls)
        deltanames = []
        deltacomment = []
        for i in range(4,4+deltaNumber*2,2):
            #print(i)
            deltanames.append(delta_urls[i])
            if delta_urls[i+1].startswith('/r/changemyview/comments/'):
                deltacomment.append("https://old.reddit.com"+delta_urls[i+1])            
            
        deltanames, deltacomment = getdeltatext(deltacomment)
        #print(deltanames)
        #print(deltacomment)
        return(deltanames, deltacomment, delta_urls)

def getdeltatext(url):
    name = []
    text = []
    for i in range(len(url)):
        #print(url[i])
        comment_area = souper(url[i]).find('div',attrs={'class':'commentarea'})
        comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
        textComm = ''
        names = ''
        for comment in comments: 
            if comment.find('form'):
                commenter = comment.find('a',attrs={'class':'author'}).text
                comment_text = comment.find('div',attrs={'class':'md'}).text
                textComm = comment_text
                names = commenter
                if textComm != '' and names!= '' and len(textComm)>500:
                    name.append(names)
                    text.append(textComm)
                    break
    return(name, text)


		
#deltaNames, deltaComments = getDeltaNames(deltalink)

def find_delta_txt(deltaNames, deltaComments, CommentText, commentName):
    deltaPost = []
    for i in range(len(CommentText)):
        for x in range(len(deltaNames)):
            if str("/u/"+commentName[i]) == deltaNames[x]:
                check1 = CommentText[i]
                check1 = check1[0:10]
                check2 = deltaComments[x]
                check2 = check2[1:11]
                if check1 == check2:
                    deltaPost.append(CommentText[i])
                    
    return(deltaPost)

#deltapost = find_delta_txt(deltaNames, deltaComments, CommentText, commentName)

from textstat.textstat import textstat
import numpy

def flesch_kincaid_comm(text):
    flesch_kincaid = []
    for i in range(len(text)):
        flesch_kincaid.append(textstat.flesch_kincaid_grade(text[i]))
    return(flesch_kincaid)

def flesch_ease_comm(text):
    flesch_ease = []
    for i in range(len(text)):
        flesch_ease.append(textstat.flesch_reading_ease(text[i]))
    return(flesch_ease)

def flesch_kincaid_OP(text):
    flesch_kincaid = textstat.flesch_kincaid_grade(text)
    return(flesch_kincaid)

def flesch_ease_OP(text):
    flesch_ease = textstat.flesch_reading_ease(text)
    return(flesch_ease)

def similarEase(easyOP, easyComm, CommentText, commentName):
    similar = []
    saveCloseComm = []

    for i in range(len(easyComm)):
        test = abs(easyOP - easyComm[i])
        if test <10:
            similar =np.append(similar,easyComm[i])
            saveCloseComm = np.append(saveCloseComm,i)
           
    return (similar, saveCloseComm)

def makeDF(post_range):
    my_data_log = []
    for num in post_range:
        OPname, OPtxt, CommentText, commentName, URL, TOPIC, deltalink, deltabot= urlSearch(num)
        if deltalink != None and len(deltalink) >0:
            print(str(num) + ") found a delta in: "+ URL)
            deltaNames, deltapost, delta_urls = getDeltaNames(deltalink, deltabot, CommentText)
            if len(deltapost)>0:
                my_data_log.append([CommentText, TOPIC,OPtxt,CommentText, deltapost])
        else:
              print(str(num) + ") no delta found in: "+ TOPIC)
    return(my_data_log)