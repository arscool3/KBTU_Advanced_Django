import asyncio
import time
from datetime import datetime


# Event Loop


async def hello(name: str):
    await asyncio.sleep(3)
    print(f'hello, {name}!')


async def run():
    coros = []
    number_of_names = int(input('Enter number of names \n'))
    for _ in range(number_of_names):
        name = input('Enter name \n')
        coros.append(hello(name))

    started = datetime.now()
    print('started', started)
    await asyncio.gather(*coros)
    endeed = datetime.now()
    print('ended', endeed)
    print('diff', endeed - started)


asyncio.run(run())

