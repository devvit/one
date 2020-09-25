#

import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor

from hxsocks.server import HandlerFactory, HXsocksHandler, UserManager, ECC


def foo():
    cert_path = os.path.join('cert.pem')

    if not os.path.exists(cert_path):
        sys.stderr.write('server cert not found, creating...\n')
        ECC(key_len=32).save(cert_path)

    user_mgr = UserManager(cert_path)
    log_level = 30
    server = 'ss://rc4-md5:123abc@0.0.0.0:10003'

    # loop = asyncio.get_event_loop()
    # loop.set_default_executor(ThreadPoolExecutor(20))
    handler = HandlerFactory(HXsocksHandler, server, user_mgr, log_level)
    coro = asyncio.start_server(handler.handle, handler.address[0], handler.address[1]) #loop=loop
    return coro
    # loop.run_until_complete(coro)
    # loop.run_forever()
