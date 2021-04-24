###Code Snippets: 
####Bootstrap for CSS
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

####From multithreading Medium Article:

async def fetch(url, session, headers):
    async with session.get(url,headers= headers) as response:
        return await response.read()
[our own code]
try:
            loop1 = asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current eve" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop1 = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(search_query))
        loop1.run_until_complete(future)

####https://docs.scrapy.org/en/latest/topics/practices.html for basic Scrapy class structure