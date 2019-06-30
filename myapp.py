#

import base64
import os
import time
import json
import sys

import asyncio
import aiohttp
import aiohttp_jinja2
import jinja2
import psutil

from aiohttp import web, WSMsgType
from aiohttp_sse import sse_response
from bs4 import BeautifulSoup

TEST_TEXT = base64.b85decode(
    "XmoUNb2=|Ca$$EaXK8e3bz*gMWpZP0ZggdCbS`6WZ7)e}Okr<CFLQNbFKuCSbY*fcb8~WYXkl_?E@N+P"
).decode()

# import uvloop

# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'


def htmlify(filename):
    with open('templates/index.html', 'r+') as f:
        soup = BeautifulSoup(f, 'html.parser')
        soup.link['href'] = ','.join([
            'data:image/x-icon;base64',
            base64.urlsafe_b64encode(
                bytes(json.dumps(json.load(open(filename))), 'utf-8')
            ).decode('utf-8')
        ])
        f.seek(0)
        f.write(str(soup))
        f.truncate()


async def on_prepare(request, response):
    print(request.headers)


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def home(request):
    return dict()


@routes.get('/hello')
async def hello(request):
    return web.json_response(dict(ver=time.ctime(os.path.getmtime('.'))))


@routes.get('/sub')
async def sub(request):
    resp = aiohttp.web.Response()
    async with aiohttp.ClientSession() as session:
        async with session.get(TEST_TEXT) as _resp:
            resp.text = base64.decodebytes((await _resp.text()).encode()).decode()

    return resp


async def sse_test(request):
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
    reader, writer = await asyncio.open_connection('127.0.0.1', 10003)
    consumer_task = asyncio.ensure_future(consumer_handler(ws, writer))
    producer_task = asyncio.ensure_future(producer_handler(ws, reader))

    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    return ws


async def consumer_handler(ws, writer):
    async for msg in ws:
        if msg.type == WSMsgType.ERROR:
            await ws.close()
            writer.close()
        elif msg.type == WSMsgType.BINARY:
            try:
                writer.write(msg.data)
                await writer.drain()
            finally:
                pass
        elif msg.type == WSMsgType.CLOSE:
            await ws.close()
            writer.close()


async def producer_handler(ws, reader):
    while True:
        if reader.at_eof():
            break
        else:
            try:
                msg = await reader.read(4096)
                if not ws.closed:
                    await ws.send_bytes(msg)
            except Exception:
                await ws.close()
                break

    # await ws.close()

app = web.Application()
# app.on_response_prepare.append(on_prepare)
# app.add_routes([web.static('/static', 'static')])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_route('GET', '/sse_test', sse_test)
app.add_routes([web.get('/s', ws_test)])
app.add_routes(routes)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        web.run_app(app, port=10080)
    else:
        htmlify(sys.argv[1])
