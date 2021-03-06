from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import requests
import time
import json
from aiohttp import ClientSession
import nest_asyncio
import asyncio
from apiStuff import fetch, run
import re
from bs4 import BeautifulSoup
nest_asyncio.apply()
bag = {"conserve",'follow','tips','reduce','recycle','should','attempt','try', 'limit','save', 'pollution','air','water','electricity','health','emission', 'oil','greenhouse','gas','green','sustainable','energy','hazard','landfill','trash','disposable','risk'}
app = Flask(__name__)
responses = None
rows = []
async def fetch(url, session, headers=None):
    async with session.get(url,headers= headers) as response:
        return await response.read()

async def run(u):
    global responses 
    tasks = []
    async with ClientSession() as session:
        responses = None
        tasks.clear()
        for query in u:
            url = f'https://api.currentsapi.services/v1/search?keywords={query}&language=en&start_date=2019-01-01&apiKey=DjA9OiUizKuRkf5MC2Abl08flhSlHIC78tAIpszXyb08gI5z'
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)

def scrape_sentences(url):
    body = ""
    try:
        response = requests.get(url)
    except requests.exceptions.ContentDecodingError:
        return ""
        
    soup = BeautifulSoup(response.text,'html.parser')
    for p in soup.select("p"):
        #for s in p.text.split("."):
        #    if len(s) > 10:
        #        sentences.append(s+".")
        body += p.text        
    #print(body)
    return body

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['POST', 'GET'])
def index():
    global rows 
    if request.method == 'POST':
        search_query = request.form['keywords'].split(",")
        print(search_query)
        rows = []
        try:
            loop1 = asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current eve" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop1 = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(search_query))
        loop1.run_until_complete(future)
        
        #print(response.json().keys())
        if responses:
            rows.append(["Title","Description","Url","Category"])
            for response in responses:
                response = json.loads(response)["news"]
                for r in response:
                    rows.append([r['title'],r['description'],r['url'],r['category'][0],""])
            return render_template('index.html',results = rows)
        else:
            return render_template('index.html',results = None)
    else:

        return render_template('index.html',results = None)

@app.route('/imperatives')
def imperatives():
    global bag
    if len(rows):
        prog = re.compile(r"""
            # Split sentences on whitespace between them.
            (?:               # Group for two positive lookbehinds.
              (?<=[.!?])      # Either an end of sentence punct,
            | (?<=[.!?]['"])  # or end of sentence punct and quote.
            )                 # End group of two positive lookbehinds.
            (?<!  Mr\.   )    # Don't end sentence on "Mr."
            (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
            (?<!  Jr\.   )    # Don't end sentence on "Jr."
            (?<!  Dr\.   )    # Don't end sentence on "Dr."
            (?<!  Prof\. )    # Don't end sentence on "Prof."
            (?<!  Sr\.   )    # Don't end sentence on "Sr."
            \s+               # Split on whitespace between sentences.
            """, 
            re.IGNORECASE | re.VERBOSE)
        sentencesGrouped = []
        for r in rows[1:]:
            sentences = ""
            body = scrape_sentences(r[2])
            sentenceList = prog.split(body)
            for sentence in sentenceList:
                if(sentence[0:sentence.find(" ")].lower() in bag):
                    sentences+=sentence+"\n"
            r[4] = sentences
            print(sentences)
            sentencesGrouped.append(sentences)
        rows[0] = ["Title","Description","Url","Category","Recs"]

        return render_template('index.html',results = rows)
    else:
        return render_template('index.html',results = None)
    
    
if __name__ == "__main__":
    app.run(debug=True)
