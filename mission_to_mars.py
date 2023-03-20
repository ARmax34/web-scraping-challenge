#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from selenium import webdriver


# In[2]:


# use splinter to open a chrome browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# get the url
url ="https://redplanetscience.com/"    


# In[4]:


# open the url
browser.visit(url)


# In[5]:


# create the html for bs
html = browser.html


# In[6]:


# create beautifulsoup object
    #Notes: bs is running a parsing function on html based on the HTML var passed to it
    #This collects the html of the target where is can be read in this program
soup = bs(html, "html.parser")


# In[7]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[8]:


# get the specific data
    #Notes: This trims down the serch with a find function in bs
data = soup.find("div", class_="col-md-12")
print(data)


# In[9]:


# use bs to get news title and paragraph info
news_title = data.find("div", class_="content_title").text
    #The .a.text will only collect the string that is clickable for the link
    
    
paragraph = data.find("div", class_="article_teaser_body").text

#Print test 1
print(news_title)
print("--------------------")
print(paragraph)


# In[10]:


# Image scrapping


# In[11]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[12]:


img_url = 'https://spaceimages-mars.com'


# In[13]:


#Basiclly a repeat from earlier with the titles, but for images

browser.visit(img_url)

html = browser.html

soup = bs(html, "html.parser")

print(soup.prettify())


# In[14]:


# use beautifulsoup to navigate to the image
image = soup.find("img", class_="headerimage fade-in")["src"]

# display larger size image
print(image)


# In[15]:


# create the url for the image
featured_image_url = "https://spaceimages-mars.com/" + image
print(featured_image_url)


# In[16]:


#Fun Facts about Mars


# In[17]:


# get the url for Mars's facts 
facts_url = "https://galaxyfacts-mars.com"

# # Use panda's `read_html` to parse the url
table = pd.read_html(facts_url)
table[1]


# In[18]:


# convert table to pandas dataframe
facts_df = table[1]
facts_df

#rename the columns
facts_df.columns=["description", "value"]
facts_df


# In[19]:


# reset the index
facts_df.set_index("description", inplace=True)
facts_df


# In[20]:


# convert dataframe
facts_html = facts_df.to_html()
print(facts_html)


# In[21]:


#Hemispheres


# In[22]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)

html = browser.html

soup = bs(html, "html.parser")

print(soup.prettify())


# In[23]:


data = soup.find_all("div", class_="item")

hemisphere_img_urls = []


# In[24]:


for d in data:
    
    title = d.find("h3").text
    
    img_url = d.a["href"]
    
    url = "https://astrogeology.usgs.gov" + img_url
    
    response = requests.get(url)
    
    soup = bs(response.text,"html.parser")
    
    new_url = soup.find("img", class_="wide-image")["src"]
    
    full_url = "https://astrogeology.usgs.gov" + new_url
    
    hemisphere_img_urls.append({"title": title, "img_url": full_url})

hemisphere_img_urls   


# In[ ]:




