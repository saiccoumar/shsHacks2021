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
bag = {'add',
 'always',
 'and',
 'apply',
 'ask',
 'assist',
 'bake',
 'be',
 'beam',
 'become',
 'believe',
 'black',
 'blind',
 'boil',
 'break',
 'breathe',
 'bring',
 'bury',
 'buy',
 'call',
 'cancel',
 'carry',
 'change',
 'check',
 'choose',
 'chop',
 'clap',
 'clean',
 'clear',
 'close',
 'collect',
 'come',
 'complete',
 'compose',
 'consider',
 'continue',
 'cook',
 'crack',
 'create',
 'cremate',
 'cross',
 'crouch',
 'cure',
 'cut',
 'decrease',
 'delete',
 'discover',
 'do',
 'do,',
 "don't",
 'dont',
 'dream',
 'drink',
 'drive',
 'driver',
 'eat',
 'edit',
 'end',
 'enjoy',
 'enrich',
 'extract',
 'fake',
 'feed',
 'feel',
 'fetch',
 'fill',
 'find',
 'finish',
 'first,',
 'flip',
 'fold',
 'forget',
 'get',
 'give',
 'go',
 'halt',
 'hand',
 'have',
 'heat',
 'help',
 'honor',
 'hum',
 'hurry',
 "i'd",
 'ignore',
 'improve',
 'include',
 'increase',
 'invade',
 'iron',
 'irrigate',
 'join',
 'jump',
 'just',
 'keep',
 'launch',
 'lead',
 'learn',
 'leave',
 'lend',
 'let',
 "let's",
 'listen',
 'live',
 'load',
 'lock',
 'look',
 'love',
 'maintain',
 'make',
 'march',
 'may',
 'meet',
 'mix',
 'mop',
 'move',
 'mute',
 'never',
 'note',
 'oh,',
 'open',
 'order',
 'overhaul',
 'pack',
 'paint',
 'park',
 'pass',
 'pause',
 'pay',
 'pick',
 'plant',
 'play',
 'please',
 'please,',
 'plow',
 'poison',
 'post',
 'pour',
 'power',
 'preheat',
 'promise',
 'push',
 'put',
 'question',
 'raid',
 'raise',
 'reach',
 'read',
 'read,',
 'reboot',
 'redo',
 'remember',
 'remind',
 'remove',
 'repair',
 'report',
 'request',
 'respect',
 'retreat',
 'return',
 'rise',
 'roar,',
 'roll',
 'run',
 'save',
 'say',
 'search',
 'season',
 'select',
 'send',
 'serve',
 'set',
 'shoot',
 'shop',
 'shout',
 'show',
 'shut',
 'silence!',
 'silence,',
 'sing',
 'sit',
 'sit,',
 'skip',
 'slap',
 'sleep',
 'slice',
 'smile',
 'softer',
 'somebody',
 'speak',
 'spy',
 'stand',
 'start',
 'stay',
 'steep',
 'stir',
 'stop',
 'study',
 'summarize',
 'suprise',
 'swich',
 'swing',
 'switch',
 'tack',
 'take',
 'take,',
 'talk',
 'taste',
 'tell',
 'then,',
 'throw',
 'touch',
 'try',
 'turn',
 'unlock',
 'unloose',
 'unmute',
 'update',
 'use',
 'visit',
 'wait',
 'wake',
 'walk',
 'wash',
 'watch',
 'wear',
 'when',
 'whisper',
 'work',
 'write',
 'write,',
 'you'}
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
