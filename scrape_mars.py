from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver

#This is the function used to start the browser in chrome
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_all():
    #Testing return
    #return {"title":"News from Mars"}

    browser = init_browser()

    url ="https://redplanetscience.com/"    

    # open the url
    browser.visit(url)

    # create the html for bs
    html = browser.html

    # create beautifulsoup object
    #Notes: bs is running a parsing function on html based on the HTML var passed to it
    #This collects the html of the target where is can be read in this program
    soup = bs(html, "html.parser")

    # get the specific data
    #Notes: This trims down the serch with a find function in bs
    data = soup.find("div", class_="col-md-12")

    # use bs to get news title and paragraph info
    news_title = data.find("div", class_="content_title").text
    #The .a.text will only collect the string that is clickable for the link

    paragraph = data.find("div", class_="article_teaser_body").text

    img_url = 'https://spaceimages-mars.com'

    #Basiclly a repeat from earlier with the titles, but for images

    browser.visit(img_url)

    html = browser.html

    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = soup.find("img", class_="headerimage fade-in")["src"]

    # create the url for the image
    featured_image_url = "https://spaceimages-mars.com/" + image

    # get the url for Mars's facts 
    facts_url = "https://galaxyfacts-mars.com"

    # # Use panda's `read_html` to parse the url
    table = pd.read_html(facts_url)

    # convert table to pandas dataframe
    facts_df = table[1]

    #rename the columns
    facts_df.columns=["description", "value"]


    # reset the index
    facts_df.set_index("description", inplace=True)


    # convert dataframe
    facts_html = facts_df.to_html()

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    html = browser.html

    soup = bs(html, "html.parser")

    data = soup.find_all("div", class_="item")

    hemisphere_img_urls = []


    for d in data:
        
        title = d.find("h3").text
        
        img_url = d.a["href"]
        
        url = "https://astrogeology.usgs.gov" + img_url
        
        response = requests.get(url)
        
        soup = bs(response.text,"html.parser")
        
        new_url = soup.find("img", class_="wide-image")["src"]
        
        full_url = "https://astrogeology.usgs.gov" + new_url
        
        hemisphere_img_urls.append({"title": title, "img_url": full_url})

    # create mars data dictionary to hold data
    data_from_mars = {
        "news_title": news_title,
        "paragraph" : paragraph,
        "featured_image_url": featured_image_url,
        "html_table": facts_html,
        "hemisphere_img_urls": hemisphere_img_urls
    }

    # close the browser after scraping
    browser.quit()

    # return results
    return data_from_mars