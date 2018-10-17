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
    name = OPname.text
    
    return(txt, OPwords, name)

def getComments(url):
    deltabot = 0
    comment_area = souper(url).find('div',attrs={'class':'commentarea'})
    comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
    extracted_comments = []
    textComm = []
    names = []
    for comment in comments: 
        if comment.find('form'):
            commenter = comment.find('a',attrs={'class':'author'}).text
            comment_text = comment.find('div',attrs={'class':'md'}).text
            #link = comment.find('a',attrs={'class':'bylink'})['href']
            extracted_comments.append({'name':commenter,'text':comment_text})
            textComm.append(comment_text)
            names.append(commenter)
        if commenter == "DeltaBot":
            deltabot = 1
    return(extracted_comments, textComm, names, deltabot)


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
        return(None,None,None,None,None, "No topic found")
    else:
        ##return all data
        URL = urls[locURL]
        OPtxt, OPwords, Opname = getOPtext(URL)
        comments, commentTXT, Names, deltabot = getComments(URL)
        return(OPname, OPtxt, commentTXT, Names, URL, TOPIC, deltabot)
