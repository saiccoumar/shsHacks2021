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

regex to extract sentences from paragraphs (copied after serious effort was put into making the regex independently)
re.compile(r"""
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