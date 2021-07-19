# dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint

def scrape():
    path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome',**path, headless=False)
    
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_article = soup.body.find_all('div', class_='content_title')[0]
    news_article = news_article.text
    news_description = soup.body.find_all('div', class_='article_teaser_body')[0]
    news_description = news_description.text
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    soup = bs(browser.html,'html.parser')
    featured_image_link = soup.find('img', class_='fancybox-image')['src']
    featured_image_link = url + featured_image_link
    
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    tables = pd.read_html(url)
    table = tables[1]
    html_table = table.to_html(index=False,header=False,justify='right',table_id='table-html-css',classes='table table-hover table-striped').replace('border="1"','border="0"')
    html_table = html_table.replace('\n','')
    
    hemisphere_image_urls = []
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    block = soup.find_all('div',class_='description')
    for x in block:
        body = x
        header = body.find('h3').text
        link = body.find('a', href=True)['href']
        url_lookup = url + link

        browser.visit(url_lookup)
        soup = bs(browser.html, 'html.parser')
        image = soup.find_all('li')[0]
        image = image.find('a',href=True)['href']
        image_url = url + image
        header_image = {"title": header, 'imageurl': image_url}
        hemisphere_image_urls.append(header_image)
        browser.links.find_by_partial_text('Back').click()
        
    browser.quit()

    mars_data = {
        "headline": news_article,
        "description": news_description,
        "featuredimage": featured_image_link,
        "marstable": html_table,
        "hemisphereimages": hemisphere_image_urls 
    }
    
    return mars_data 




