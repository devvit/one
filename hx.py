#

import os
import sys
import asyncio

from hxsocks.server import HandlerFactory, HXsocksHandler, UserManager, ECC

from ws_to_tcp import WsServerToTCPClient
from tcp_to_ws import TCPServerToWsClient


def foo():
    cert_path = os.path.join('cert.pem')

    if not os.path.exists(cert_path):
        sys.stderr.write('server cert not found, creating...\n')
        ECC(key_len=32).save(cert_path)

    user_mgr = UserManager(cert_path)
    log_level = 30
    server = 'ss://rc4-md5:123abc@0.0.0.0:10003'

    # loop.set_default_executor(ThreadPoolExecutor(20))
    handler = HandlerFactory(HXsocksHandler, server, user_mgr, log_level)
    coro = asyncio.start_server(handler.handle, handler.address[0], handler.address[1])
    return coro


if __name__ == '__main__':
    """
    z = TCPServerToWsClient(
        ws_ip='0.0.0.0',
        ws_port=10000,
        tcp_ip='localhost',
        tcp_port=10003,
        path='/',
        chunk_size=4096
    )
    """
    z = WsServerToTCPClient(
        ws_ip='0.0.0.0',
        ws_port=10000,
        tcp_ip='localhost',
        tcp_port=10003,
        chunk_size=4096
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(foo())
    loop.run_until_complete(z.server())
    loop.run_forever()
