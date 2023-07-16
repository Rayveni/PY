import asyncio
import aiohttp
import datetime
# https://superfastpython.com/python-asyncio/#Write_HTTP_Request
url_list = ['https://zelenka.guru/threads/3008577/?pget=3',
            'https://zelenka.guru/threads/3008577/?pget=1']


class rate_limit(object):
    def __init__(self, calls=5, period=1):
        self.calls = calls
        self.period = period
        self.clock = asyncio.get_event_loop().time
        self.last_reset = 0
        self.num_calls = 0

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            if self.num_calls >= self.calls:
                await asyncio.sleep(self.__period_remaining())
            period_remaining = self.__period_remaining()
            if period_remaining <= 0:
                self.num_calls = 0
                self.last_reset = self.clock()
            self.num_calls += 1
            return await func(*args, **kwargs)
        return wrapper

    async def limiter(self, func, *args, **kwargs):
        if self.num_calls >= self.calls:
            await asyncio.sleep(self.__period_remaining())
        period_remaining = self.__period_remaining()
        if period_remaining <= 0:
            self.num_calls = 0
            self.last_reset = self.clock()
        self.num_calls += 1
        return await func(*args, **kwargs)

    def __period_remaining(self):
        print(self.clock(), self.last_reset)
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed

# @rate_limit(calls=1, period=10)
async def fetch(url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}
    try:
        async with session.get(url, headers=headers) as response:
            content = await response.read()
            return (url, 'OK', content)
    except Exception as e:
        print(e, url)
        return (url, 'ERROR', str(e))

async def run(url_list):
    r_l = rate_limit(7, 1)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(r_l.limiter(
            fetch, url, session)) for url in url_list]

        responses = asyncio.gather(*tasks)
        await responses
        print(responses)

    return responses

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
task = asyncio.ensure_future(run(url_list))
loop.run_until_complete(task)
result = task.result().result()


"""# coroutine used for the entry point
async def main():
    # report a message
    print('main starting')
    # create group level 1
    group1 = asyncio.gather(task_coro(0), task_coro(1), task_coro(2))
    # create group level 2
    group2 = asyncio.gather(task_coro(3), task_coro(4), task_coro(5))
    # create group level 3
    group3 = asyncio.gather(group1, group2)
    # execute 3, which executes 1 and 2
    await group3
    # report a message
    print('main done')
"""
