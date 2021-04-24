import time
import json
from aiohttp import ClientSession
import nest_asyncio
import asyncio
import requests

indexes = {}
index = 0
async def fetch(url, session, headers=None):
    async with session.get(url,headers= headers) as response:
        return await response.read()

async def run(u):
    #global responses  
    tasks = []
    async with ClientSession() as session:
        responses = None
        tasks.clear()
        for query in u:
            url = f'https://api.currentsapi.services/v1/search?keywords={query}&language=en&apiKey=DjA9OiUizKuRkf5MC2Abl08flhSlHIC78tAIpszXyb08gI5z'
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        responses = [j["news"] for j in responses]

