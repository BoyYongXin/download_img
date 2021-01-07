# -*- coding:utf-8 -*-
# @Author: Mr.Yang
# @Date: 2020/4/1 pm 2:37
# @email: 1426866609@qq.com

import sys
import asyncio
from loguru import logger
import traceback
import time
import httpx
from dataclasses import dataclass
import os
import redis
import re
import requests
import pymongo

DEST_DIR = "/Users/admin/pworkspace/videos/"


def run_time(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        logger.info(f"当前任务运行时间{time.time() - start}")

    return wrapper


def debug(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as err:
            logger.error(err)
            traceback.print_exc()

    return wrapper


@dataclass
class maintain_download(object):
    num: int = 0
    sleep_time: int = 60
    time_out: int = 15
    max_keepalive_connections: int = 50
    max_connections: int = 50

    @debug
    async def maintain_download(self):

        # MONGO_HOST = 'rs_cralwer_01.mongo.int.yidian-inc.com:27017,rs_cralwer_02.mongo.int.yidian-inc.com:27017,rs_cralwer_03.mongo.int.yidian-inc.com:27017'
        # MONGO_HOST = 'rs_xuanpin_01.mongo.int.yidian-inc.com:27017,rs_xuanpin_02.mongo.int.yidian-inc.com:27017,rs_xuanpin_03.mongo.int.yidian-inc.com:27017'
        # mongo_conn = pymongo.MongoClient(MONGO_HOST, connect=False)
        # db = mongo_conn.xuanpin
        # # collection = db.zhidemai_news
        # collection = db.weibo_duanneirong
        # user_list = collection.find({}, no_cursor_timeout=True).sort([("insert_time", -1)]).limit(2000)
        # for item in user_list:
        #     content = item["content"]
        #     # regex = r'(http.:[\S]*?.(jpg|jpeg|png|gif|bmp|webp)")'
        #     regex = r'(http.:[\S]*?.(jpg|jpeg|png)")'
        #     try:
        #         imgs = re.findall(regex, content, re.S | re.M)
        #         print(imgs)
        #         # if imgs:
        #         #     await asyncio.gather(*[self.get_html(pattern[0]) for pattern in imgs])
        #         #     await asyncio.sleep(0.1)
        #         #     continue
        #         # else:
        #         #     continue
        #
        #     except Exception as err:
        #         logger.error(err)
        ## 油果视频 ##
        MONGO_HOST = 'rs_xuanpin_01.mongo.int.yidian-inc.com:27017,rs_xuanpin_02.mongo.int.yidian-inc.com:27017,rs_xuanpin_03.mongo.int.yidian-inc.com:27017'
        mongo_conn = pymongo.MongoClient(MONGO_HOST, connect=False)
        db = mongo_conn.xuanpin
        # collection = db.zhidemai_news
        collection = db.youguo_video
        user_list = collection.find({"$or": [{"resolution": "720P"}, {"resolution": "1080P"}]},
                                    no_cursor_timeout=True).sort([("insert_time", -1)]).limit(200)
        # video_urls = []
        for item in user_list:
            # video_urls.append((item["url"],item["title"]))
            video_urls = [(item["url"], item["title"])]

            try:
                await asyncio.gather(*[self.get_html(pattern) for pattern in video_urls])
                await asyncio.sleep(3)
            except Exception as err:
                logger.error(err)

    async def save_flag(self, img, filename):
        self.show(img)
        path = os.path.join(DEST_DIR, filename)
        with open(path, 'wb') as fp:
            fp.write(img)
        logger.info("下载成功")

    def show(self, text):  # <7>
        # print(text, end=' ')
        sys.stdout.flush()

    def re_sting_title(self, str):
        # str = re.sub("[$a-zA-Z|\!\%\[\]\,\。\?\'\"\@\.\*\&\、\:\;\$\\\|a-zA-Z$]", "", str)
        str = re.sub("[\!\%\[\]\,\。\?\'\"\@\*\&\、\:\;\$\\\\/]", "", str)
        return str

    async def get_html(self, pattern):
        logger.info(f"正在下载 : {pattern}")
        # max_keepalive，允许的保持活动连接数或 None 始终允许。（预设10）
        # max_connections，允许的最大连接数或 None 无限制。（默认为100）
        limits = httpx.Limits(max_keepalive_connections=self.max_keepalive_connections,
                              max_connections=self.max_connections)
        url = pattern[0]
        name = self.re_sting_title(pattern[1]) + ".mp4"
        try:
            async with httpx.AsyncClient(limits=limits, timeout=self.time_out) as client:
                resp = await client.get(url)
                assert resp.status_code == 200
                await self.save_flag(resp.read(), name)
        except Exception as err:
            logger.error(f"下载失败 url : {url}, err: {err}")
            return
        else:
            self.num += 1
