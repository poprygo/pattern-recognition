import websockets
import asyncio
import json
import numpy as np
import doctest

def median(arr, repeats):
    """
    >>> median([43,1,1,1], 3)
    [0, 0, 0]
    >>> median([3,103,123,113], 3)
    [2, 2, 2]
    >>> median([34, 138, 69, 1, 1], 5)
    [1, 1, 1, 1, 1]
    """
    sum_arr = np.array(arr).sum()
    prob = [i / sum_arr for i in arr]

    res = 0
    guesses = []

    for i in range(len(arr)):
        res += prob[i]
        if res >= 1 / 2:
            for j in range(repeats):
                guesses.append(i)
            break
    return guesses


async def second_task():
    uri = "wss://sprs.herokuapp.com/second/Yaroslav"
    async with websockets.connect(uri) as websocket:

        width = int(input("weight: "))
        if 2 >= width >= 1000:
            print("error width")
            width = int(input("weight: "))
        totalSteps = int(input("total steps: "))
        if 1 >= totalSteps >= 1000000:
            print("error total steps")
            totalSteps = int(input("total steps: "))
        repeats = int(input("repeats: "))
        if 1 >= repeats >= 1000:
            print("error repeats")
            repeats = int(input("repeats: "))

        a1 = json.dumps({"data": {"width": width, "loss": "L1", "totalSteps": totalSteps, "repeats": repeats}})
        await websocket.send(a1)
        a2 = await websocket.recv()

        print(f">>> {a1}\n<<< {a2}")

        for i in range(totalSteps):
            a3 = json.dumps({"data": {"message": "Ready"}})
            await websocket.send(a3)
            a4 = await websocket.recv()

            print(f">>> {a3}\n<<< {a4}")

            a5 = json.dumps({"data": {"step": i + 1, "guesses": median(json.loads(a4)["data"]["heatmap"], repeats)}})
            await websocket.send(a5)
            a6 = await websocket.recv()

            print(f">>> {a5}\n<<< {a6}")

        a7 = json.dumps({"data": {"message": "Bye"}})
        await websocket.send(a7)
        a8 = await websocket.recv()

        print(f">>> {a7}\n<<< {a8}")


if __name__ == "__main__":
    doctest.testmod()
    asyncio.get_event_loop().run_until_complete(second_task())
