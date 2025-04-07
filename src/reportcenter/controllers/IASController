#coding=utf-8
# @Time    : 2023/10/12 17:00
# @Author  : zack wang

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from reportcenter.models import search_stock_model

import asyncio

app = FastAPI()

async def async_generator(text:str):
    for char in text:
        await asyncio.sleep(0.05)
        yield char

@app.get("/serach_stock/{stock_code}")
async def search_stock(stock_code: str):
    text = search_stock_model.search_stock(stock_code)
    return StreamingResponse(async_generator(text))

if __name__ == '__main__':
    app.run(port=5000)