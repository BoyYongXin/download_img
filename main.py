# -*-coding=utf-8 -*-
import sys
import asyncio
from async_download_data import maintain_download
from loguru import logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


def run_maintainer():
    """
    下载器主入口
    :return:
    """
    download = maintain_download()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download.maintain_download())
    logger.info(f"下载成功了{download.num}个数据")


if __name__ == '__main__':
    run_maintainer()
