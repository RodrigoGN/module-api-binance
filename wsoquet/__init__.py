from websockets import connect
import asyncio
import json

coins = ["BTCUSDT", "BNBUSDT"]
coinPrice = {}

async def conexao(args, metod="bookTicker"):
    """
    metod = bookTicker, bookTicker24h, bookTickerL2, bookTickerL224h
    args = lista de coins
    """
    async with connect(f'wss://stream.binance.com:9443/ws/{metod}') as ws:
        if type(args) == type(list()):
            [await ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{a.lower()}@ticker"], "id": 1})) for a in args]
        elif type(args) == type(dict()):
            lista = args.values()
            [await ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{i.lower()}@ticker"], "id": 1})) for i in lista]
        else:
            await ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{args.lower()}@ticker"], "id": 1}))
        while True:
            msg = json.loads(await ws.recv())
            if 'a' in msg:
                coinPrice[msg['s']] = {'Ask': msg['a'], 'Bid': msg['b']}
                print(coinPrice)


if __name__ == "__main__":
    asyncio.run(conexao(coins))
