import concurrent.futures as future
import _thread
import socket
import asyncio
import functools
import time
import datetime
from typing import Callable
import pickle


def make_async(fn: Callable) -> Callable:
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(fn, *args, **kwargs)
    return wrapper


def timeout(fn: Callable, timeout_: float = 2) -> Callable:
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await asyncio.wait_for(fn(*args, **kwargs), timeout=timeout_)
        except TimeoutError:
            return tuple()
    return wrapper


@timeout
@make_async
def check_addr(ip: str) -> tuple:
    """
    check if IPv4 is findable, return valid address name
    :param ip: IPv4 address
    :return: host name and address
    """
    try:
        return socket.gethostbyaddr(ip)
    except socket.gaierror:
        return tuple()
    except socket.herror:
        return tuple()


async def find_devices():
    """
    find devices on local network
    :return:
    """
    loop = asyncio.get_running_loop()
    loop.set_default_executor(future.ThreadPoolExecutor(max_workers=1000))
    addr = socket.gethostbyname(socket.gethostname())
    index = addr.rfind('.')
    base = addr[:index+1]
    args = [base + str(i) for i in range(1000)]
    tasks = [check_addr(x) for x in args]
    results = await asyncio.gather(*tasks)
    devices = {x[0].lower(): x[2] for x in results if x}
    print('devices: ')
    for key in devices:
        print(f'{key}: {devices[key]}')


if __name__ == '__main__':
    asyncio.run(find_devices())
