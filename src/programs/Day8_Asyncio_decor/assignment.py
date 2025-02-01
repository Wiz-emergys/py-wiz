import asyncio
import timeit 
import aiohttp

def log_execution_time(func):
    async def wrapper(*args,**kargs):
        start=timeit.default_timer()
        print(f"started feching {args[0]}")
        result=await func(*args,**kargs)
        total=timeit.default_timer()-start
        print(f"completed fetching {args[0]} it took {total} sec")
        return result
    return wrapper


@log_execution_time
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.json


async def main():
    urls=[ "https://jsonplaceholder.typicode.com/users/6",
        "https://jsonplaceholder.typicode.com/users/4",
        "https://jsonplaceholder.typicode.com/todos/19" ]
    
    results=await asyncio.gather(*(fetch_url(url) for url in urls ))

    for url,result in zip(urls,results):
        print(f"Response from {url} is {result}\n")

if __name__=="__main__" :
    asyncio.run(main())