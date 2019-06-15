#

import os
import time
import json

import asyncio
import aiohttp_jinja2
import jinja2

import psutil

from aiohttp import web
from aiohttp_sse import sse_response

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'


async def on_prepare(request, response):
    print(request.headers)


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    return dict(ver='0101')


async def sse_test(request):
    # loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            s0 = psutil.net_io_counters(pernic=True)[device].bytes_recv
            await asyncio.sleep(1)
            s1 = psutil.net_io_counters(pernic=True)[device].bytes_recv
            s3 = s1 - s0
            now = int(time.time())
            await resp.send(json.dumps([
                dict(time=now, y=s3),
                dict(time=now, y=s1),
                dict(time=now, y=psutil.cpu_percent()),
                dict(time=now, y=psutil.virtual_memory().percent)
            ]))
    return resp


async def ws_test(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        pass

    return ws


app = web.Application()
app.on_response_prepare.append(on_prepare)
# app.add_routes([web.static('/static', 'static')])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_route('GET', '/sse_test', sse_test)
# app.add_routes([web.get('/ws_test', ws_test)])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5000)
