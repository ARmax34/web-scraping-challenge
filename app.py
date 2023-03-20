#import datetime as dt
#import numpy as np
from flask_pymongo import PyMongo
import scrape_mars
from flask import Flask, jsonify, render_template, redirect

app = Flask(__name__)


#Establishing MDB connection
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#/scrape
#mars_dic = {}

#This should get the scrapping data from MDB
#Do not use mars_dic var
@app.route("/")
def index():
    info = mongo.db.mars_collection.find_one()


    #return from templates folder -> index file
    return render_template("index.html", data_from_mars = info)


    #Testing 
    #if not mars_dic:
        #scrape()
    #return from templates folder -> index file
    #return render_template("index.html", data_from_mars = mars_dic)

#This function should not use a global var
        #testing
#@app.route("/scrape")
#def scrape():
    #global mars_dic
    #mars_dic = scrape_all()
    #print("I am scraping")
    #return index()





@app.route("/scrape")
def scrape():
    data_from_mars = scrape_mars.scrape_all()
    mongo.db.mars_collection.update({}, data_from_mars, upsert=True)
    #return index()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)