#

import os
import time
import subprocess
import json

import asyncio
import aiohttp_jinja2
import jinja2

import psutil

from aiohttp import web

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'


async def get_bytes():
    p = await asyncio.create_subprocess_shell(
        f'cat /sys/class/net/{device}/statistics/rx_bytes',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    return int((await p.communicate())[0])


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    return {}


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        s0 = await get_bytes()
        await asyncio.sleep(1)
        s1 = await get_bytes()
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
app.add_routes([web.get('/ws', websocket_handler)])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5000)
