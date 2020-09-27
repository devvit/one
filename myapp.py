#

import asyncio
import base64
import json
import os
import time

import aiohttp
import aiohttp_jinja2
import jinja2
import psutil

from aiohttp import web, WSMsgType
from aiohttp_sse import sse_response
from aiojobs.aiohttp import setup, spawn
from bs4 import BeautifulSoup
from siosocks.io.asyncio import socks_server_handler

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}


def htmlify(filename):
    dest = 'templates/index.html'
    html_str = open(dest).read()
    soup = BeautifulSoup(html_str, 'html.parser')
    links = soup.select('link[type="image/x-icon"]')
    if len(links) > 0:
        links[0].extract()

    iconx = soup.new_tag('link')
    iconx['rel'] = 'icon'
    iconx['type'] = 'image/x-icon'
    iconx['href'] = ','.join([
        'data:image/x-icon;base64',
        base64.urlsafe_b64encode(
            bytes(json.dumps(json.load(open(filename))), 'utf-8')
        ).decode('utf-8')
    ])
    soup.title.insert_after(iconx)
    with open(dest, 'w') as f:
        f.write(soup.prettify())


async def on_startup(app):
    pass


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def home(request):
    return dict()


@routes.get('/world')
async def world(request):
    resp = aiohttp.web.Response()

    if 'url' in request.query:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(request.query['url']) as _resp:
                resp.text = await _resp.text()

    return resp


async def hello_handler(request):
    async with sse_response(request) as resp:
        while True:
            s0 = psutil.net_io_counters(pernic=True)[device].bytes_recv
            await asyncio.sleep(1)
            s1 = psutil.net_io_counters(pernic=True)[device].bytes_recv
            s3 = s1 - s0
            now = int(time.time())
            proc = psutil.Process()
            await resp.send(json.dumps([
                dict(time=now, y=s3),
                dict(time=now, y=s1),
                dict(time=now, y=psutil.cpu_percent()),
                dict(time=now, y=proc.memory_info().rss)
            ]))

    return resp


async def coro_func(info):
    # await asyncio.sleep(3.0)
    print('***')
    await asyncio.create_subprocess_shell(info['script'])
    print('---')


async def job_handler(request):
    milk = await request.json()
    await spawn(request, coro_func(milk))

    return web.json_response(dict(ok=True))


# https://github.com/iwanders/ws_bridge
async def ws_handler(request):
    ws = web.WebSocketResponse(protocols=['binary'])
    await ws.prepare(request)
    reader, writer = await asyncio.open_connection('localhost', 10003)
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


def create_app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.start_server(socks_server_handler, port=10003))

    app = web.Application()
    app.on_startup.append(on_startup)
    # app.on_response_prepare.append(on_prepare)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    setup(app)
    app.add_routes([web.static('/static', 'static')])
    app.router.add_get('/hello', hello_handler)
    # app.router.add_post('/cow', job_handler)
    app.add_routes([web.get('/ws', ws_handler)])
    app.add_routes(routes)

    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=os.environ['HTTP_PORT'])
