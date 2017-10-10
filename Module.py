import time, sys, math, requests, bs4, json, urllib
from bs4 import BeautifulSoup
    

# showName has to be of form 'friends' or 'the-big-bang-theory'

def mainFunction(showName):         
    showData = requests.get("http://api.tvmaze.com/singlesearch/shows?q="+showName)
    showData = showData.json()
    showId = showData["id"]

    seasonData = requests.get("http://api.tvmaze.com/shows/"+str(showId)+"/seasons")
    seasonData = seasonData.json()
    
    for i in range(len(seasonData)):
        seasonId = seasonData[i]['id']
        print(seasonId)        
        seasonDownload(seasonId, showName)

def seasonDownload(seasonId, showName):
    episodeList = requests.get("http://api.tvmaze.com/seasons/"+str(seasonId)+"/episodes")
    episodeList = episodeList.json()
    seasonNumber = episodeList[1]['season']
    for j in range(len(episodeList)):
        episodeUrl = episodeList[j]['url']
        episodeTag_1 = episodeUrl[episodeUrl.find(showName)+len(showName)+1:].strip()
        episodeTag = episodeTag_1[episodeTag_1.find('-')+1:].strip()
        if j<9:
            episodeNumber = '0' + str(j+1);
        else:
            episodeNumber = str(j+1)
        fmoviesString = showName + '-season-' + str(seasonNumber) + '-episode-' + episodeNumber + '-' + episodeTag
        print(j+1)
        downloadEpisode(fmoviesString)

def downloadEpisode(fmoviesString):
    url_fmovies = 'https://www.fmovies.io/watch/' + fmoviesString + '.html'
    res = requests.get(url_fmovies)
    bsObject = bs4.BeautifulSoup(res.text, "html.parser")
    elems = bsObject.find_all(class_='player current')
    data = []

    for charac in elems:
        data.append(str(charac))

    data = data[0]
    data = data[data.find('src="')+5:].strip()
    data = data[:data.find('"')].strip()

    print(data)

mainFunction('friends')
