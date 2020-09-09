import pymongo
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time   

def scrape():

    executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    marsNewsUrl = 'https://mars.nasa.gov/news/'
    browser.visit(marsNewsUrl)
    time.sleep(2)

    html = browser.html
    soup = bs(html,'html.parser')

    allSlides = soup.find_all('div', class_="list_text")
    rootUrl = 'https://mars.nasa.gov'

    titles = []
    dates = []
    previews = []
    links = []

    for slide in allSlides:
        listDate = slide.find('div',class_="list_date")
        slideTitle = slide.find('div',class_="content_title")
        title = slideTitle.find('a')
        link = rootUrl + title['href']
        preview = slide.find('div', class_="article_teaser_body")
    
        titles.append(title.text)
        dates.append(listDate.text)
        links.append(link)
        previews.append(preview.text)
    
    slideData = {'Title': titles, 'Date': dates, 'Link': links, 'Preview': previews}
    slideDf = pd.DataFrame(data=slideData)

    # Latest news
    latestArticleTitle = slideDf.Title[0]
    latestArticlePreview = slideDf.Preview[0]

    MarsPicUrl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(MarsPicUrl)
    html = browser.html
    soup = bs(html,'html.parser')
    rootImgUrl = 'https://www.jpl.nasa.gov'
    
    allImages = soup.find_all('a', class_="fancybox")
    marsImg = []
    for img in allImages:
        curImg = img['data-fancybox-href']
        curUrl = rootImgUrl + curImg
        marsImg.append(curUrl)
    
    # feature image
    featured_image_url = marsImg[10]  

    marsFactUrl = 'https://space-facts.com/mars/'
    browser.visit(marsFactUrl)  
    html = browser.html
    soup = bs(html,'html.parser')
    marsFact = pd.read_html(marsFactUrl)
    marsFactDf = marsFact[0]
    marsFactDf.columns = ['Fact', 'Value']

    # mars fact
    marsFactDf= marsFactDf.set_index('Fact')

    marsHemiUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(marsHemiUrl)
    html = browser.html
    soup = bs(html,'html.parser')

    allHemi = soup.find_all('div', class_="description")
    rootUrl = 'https://astrogeology.usgs.gov'

    hemiTitles = []
    hemiMainUrl = []

    # print the first 5 recent artciles/slides
    for hemi in allHemi:
        linkRef = hemi.find('a')
        link =  rootUrl + linkRef['href']
        title = hemi.find('h3').text
    
        hemiTitles.append(title)
        hemiMainUrl.append(link)
    
    zipHemi = list(zip(hemiTitles,hemiMainUrl))

    marsHemiImg = []
    for curTitle, curMainUrl in zipHemi:
        browser.visit(curMainUrl)
        html = browser.html
        soup = bs(html,'html.parser')
        curHemi = soup.find('div', class_="wide-image-wrapper").find('a')
        curHemiLink = curHemi['href']
        curDict = {'title': curTitle, 'image_url': curHemiLink}
        # mars dict with hemisphere images
        marsHemiImg.append(curDict)

    returnList = [{'latestArticle':latestArticleTitle},{'latestArticlePreview':latestArticlePreview},{'marsFactTable': marsFactDf },{'featureImg':featured_image_url},{'hemiImg':marsHemiImg}]

    return returnList

marsScrape = scrape()