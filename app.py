from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import requests
import time
import json
from aiohttp import ClientSession
import nest_asyncio
import asyncio
from apiStuff import fetch, run
nest_asyncio.apply()
app = Flask(__name__)
responses = None

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
            url = f'https://api.currentsapi.services/v1/search?keywords={query}&language=en&apiKey=DjA9OiUizKuRkf5MC2Abl08flhSlHIC78tAIpszXyb08gI5z'
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)

@app.route('/', methods=['POST', 'GET'])
def index():
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
            for response in responses:
                response = json.loads(response)["news"]
                for r in response:
                    rows.append((r['title'],r['description'],r['url'],r['category'][0]))
            return render_template('index.html',results = rows)
        else:
            return render_template('index.html',results = None)
    else:

        return render_template('index.html',results = None)

if __name__ == "__main__":
    app.run(debug=True)
