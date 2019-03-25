#

import os
import time
import json

import asyncio
import aiohttp_jinja2
import jinja2

import psutil

from aiohttp import web

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    return dict(ver='0325')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        s0 = psutil.net_io_counters(pernic=True)[device].bytes_recv
        await asyncio.sleep(1)
        s1 = psutil.net_io_counters(pernic=True)[device].bytes_recv
        s3 = s1 - s0
        now = int(time.time())
        await ws.send_str(json.dumps([
            dict(time=now, y=s3),
            dict(time=now, y=s1),
            dict(time=now, y=psutil.cpu_percent()),
            dict(time=now, y=psutil.virtual_memory().percent)
        ]))

    return ws


app = web.Application()
app.add_routes([web.static('/static', 'static')])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([web.get('/test', websocket_handler)])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5000)
