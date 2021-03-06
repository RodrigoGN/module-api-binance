from websockets import connect
from time import sleep
from work_ import *
from api import *
import asyncio
import json
import os

coins = ["BTCUSDT", "BNBUSDT", "BTCBUSD"]
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
            try:
                msg = json.loads(await ws.recv())
                if 'a' in msg:
                    coinPrice[msg['s']] = {'Ask': msg['a'], 'Bid': msg['b']}
                    print(coinPrice)
                    fila, event = get_task([i for i in coinPrice.keys()])
                    thrs = get_pool(len(coinPrice), target=startTrade, queue=fila, event=event)
                    [th.start() for th in thrs]
                    [th.join() for th in thrs]
            except Exception as e:
                print(f"\n{e}\n")
                break


def startTrade(coin):
    '''Adicionar aqui suas regras de negócio'''
    
    '''exemplo de compra'''
    if float(coinPrice[str(coin)]['Ask']) > (float(coinPrice[str(coin)]['Bid']) * 1.01):
        print(f'\nBuy: {coin}\n')
        
    '''exemplo de venda'''
    if float(coinPrice[str(coin)]['Ask']) < (float(coinPrice[str(coin)]['Bid']) * 0.99):
        print(f'\nSell: {coin}\n')
    

if __name__ == "__main__":
    while True:
        asyncio.run(conexao(coins, metod="bookTicker"))
