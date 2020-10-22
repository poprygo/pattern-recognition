import asyncio
import websockets
import json
import random
import doctest

from math import log
import numpy as np
from operator import xor


def logical_xor(a, b):
    """
    >>> logical_xor(0, 1)
    1
    >>> logical_xor(1, 1)
    0
    """
    assert a == 0 or a == 1
    assert b == 0 or b == 1

    return bool(a) ^ bool(b)


def first(etalons, number, p):

    value = {}

    for k in range(len(etalons)):
        result = 0

        etalons[str(k)] = np.array(etalons[str(k)])
        digit = np.array(number)

        for i in range(len(digit)):
            for j in range(len(digit[0])):
                if p != 1 and p != 0:
                    result += logical_xor(number[i][j], etalons[str(k)][i][j]) * log(p) + logical_xor(logical_xor(1, number[i][j]), etalons[str(k)][i][j]) * log(1 - p)
                elif p == 1:
                    result += logical_xor(number[i][j], etalons[str(k)][i][j])
                elif p == 0:
                    result += logical_xor(logical_xor(1, number[i][j]), etalons[str(k)][i][j])

        value[str(k)] = result

    return max(value, key=value.get)

# function hello was obtained from https://websockets.readthedocs.io/en/stable/intro.html


async def hello():
    uri = "wss://sprs.herokuapp.com/first/Yaroslav"
    async with websockets.connect(uri) as websocket:

        a1 = json.dumps({"data": {"message": "Let's start"}})
        await websocket.send(a1)

        a2 = await websocket.recv()
        print(f"\n >>>:", a1,"\n <<<:", json.loads(a2))

        width = 20
        if 0 >= width >= 100:
            print('width must be between 1 and 100')

        height = 20
        if 0 >= height >= 100:
            print('height must be between 1 and 100')

        total_steps = 10
        if 0 >= total_steps >= 1000000:
            print('total_steps must be between 1 and 1 000 000')

        p = 0
        if 0 >= p >= 1 :
            print('noise must be between 0 and 1')

        a3 = json.dumps({"data": {"width": width, "height": height, "totalSteps": total_steps, "noise": p, "shuffle": False}})

        await websocket.send(a3)
        a4 = await websocket.recv()
        print(f"\n >>>:", a3,"\n <<<:", json.loads(a4))

        for i in range(total_steps):

            a5 = {"data": {"message": "Ready"}}
            await websocket.send(json.dumps(a5))
            a6 = await websocket.recv()
            print(f"\n >>>:", a5,"\n <<<:", json.loads(a6))

            a7 = first(etalons=json.loads(a4)["data"], number= json.loads(a6)["data"]["matrix"], p=p)
            a8 = {"data": {"step": i + 1, "answer": a7}}

            await websocket.send(json.dumps(a8))
            a9 = await websocket.recv()
            print(f"\n >>>:", a8,"\n <<<:", json.loads(a9))

        a10 = json.dumps({"data": {"message": "Bye"}})
        await websocket.send(a10)
        a11 = await websocket.recv()
        print(f"\n >>>:", a10, "\n <<<:", json.loads(a11))

        # print(json.loads(response)['data']['height'])

if __name__ == "__main__":
    doctest.testmod()
    asyncio.get_event_loop().run_until_complete(hello())
