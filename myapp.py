#

import asyncio
import base64
import json
import os
import platform
import sys
import time

import aiohttp
import aiohttp_jinja2
import jinja2
import psutil

from aiohttp import web, WSMsgType
from aiohttp_sse import sse_response
from bs4 import BeautifulSoup

# import uvloop

# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

routes = web.RouteTableDef()
device = os.getenv('DEVICE') or 'lo'


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


async def on_prepare(request, response):
    print(request.headers)


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def home(request):
    return dict()


@routes.get('/hello')
async def hello(request):
    return web.json_response(dict(
        _ver=os.popen('./bower -version').read().split()[1] if os.path.exists('bower') else '0.0.0',
        ver=time.ctime(os.path.getmtime('.')) + "-PYTH0N-" + platform.python_version()
    ))


@routes.get('/world')
async def world(request):
    resp = aiohttp.web.Response()
    text = ''

    if request.query['url']:
        async with aiohttp.ClientSession() as session:
            async with session.get(request.query('url')) as _resp:
                resp.text = await _resp.text()

        return resp

    _urls = base64.b64decode(request.query['urls'].encode()).decode().strip().split(',')
    urls = list(filter(len, _urls))

    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as _resp:
                text += base64.b64decode(((await _resp.text()) + '===').encode()).decode().strip()

    resp.text = base64.b64encode(text.encode()).decode()
    return resp


async def test_handler(request):
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


async def ws_handler(request):
    ws = web.WebSocketResponse()
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


app = web.Application()
# app.on_response_prepare.append(on_prepare)
app.add_routes([web.static('/static', 'static')])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_route('GET', '/test', test_handler)
app.add_routes([web.get('/ww', ws_handler)])
app.add_routes(routes)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        web.run_app(app, port=10000)
    else:
        htmlify(sys.argv[1])
