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
                elif noise == 1:
                    result += logical_xor(number[i][j], etalons[str(k)][i][j])
                elif noise == 0:
                    result += logical_xor(logical_xor(1, number[i][j]), etalons[str(k)][i][j])

        value[str(k)] = res

    return max(value, key=value.get)

# function hello was obtained from https://websockets.readthedocs.io/en/stable/intro.html


async def hello():
    uri = "wss://sprs.herokuapp.com/first/Yaroslav"
    async with websockets.connect(uri) as websocket:

        a1 = json.dumps({"data": {"message": "Let's start"}})
        await websocket.send(a1)

        response = await websocket.recv()
        print(f"\n >>>:", a1,"\n <<<:", json.loads(response))

        width = int(input("width: "))
        if 0 >= width >= 100:
            print('width must be between 1 and 100')
            width = int(input('width: '))

        height = int(input('height: '))
        if 0 >= height >= 100:
            print('height must be between 1 and 100')
            height = int(input('height: '))

        total_steps = int(input('total_steps: '))
        if 0 >= total_steps >= 1000000:
            print('total_steps must be between 1 and 1 000 000')
            total_steps = int(input('total_steps: '))

        p = float(input('noise: '))
        if 0 >= p >= 1 :
            print('noise must be between 0 and 1')
            p = float(input('noise: '))

        a2 = json.dumps({"data": {"width": width, "height": height, "totalSteps": total_steps, "noise": p, "shuffle": False}})

        await websocket.send(a2)
        response = await websocket.recv()
        print(f"\n >>>:", a2,"\n <<<:", json.loads(response))

        for i in range(total_steps):
            k ={"data": {"message": "Ready"}}
            await websocket.send(json.dumps(k))
            response = await websocket.recv()
            print(f"\n >>>:", k,"\n <<<:", json.loads(response))

            result = str(1)
            print('result:', result)

            a3 = {"data": {"step": i + 1, "answer": str(result)}}

            await websocket.send(json.dumps(a3))
            response = await websocket.recv()
            print(f"\n >>>:", a3,"\n <<<:", json.loads(response))

        bye = json.dumps({"data": {"message": "Bye"}})
        await websocket.send(bye)
        response = await websocket.recv()
        print(f"\n >>>:", bye, "\n <<<:", json.loads(response))

        # print(json.loads(response)['data']['height'])

if __name__ == "__main__":
    doctest.testmod()
    asyncio.get_event_loop().run_until_complete(hello())
