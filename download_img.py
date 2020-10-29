# coding="utf-8"
import sys

sys.path.append("../")
import os
from loguru import logger as log
from urllib import request
import pymongo
import re
import requests

# from config import conf


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        pass


def download_file(url, base_path, filename='', call_func=''):
    file_path = base_path + filename
    directory = os.path.dirname(file_path)
    mkdir(directory)

    # 进度条
    def progress_callfunc(blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum : 已经下载的数据块
        @blocksize : 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        # print ('进度条 %.2f%%' % percent, end = '\r')
        sys.stdout.write('进度条 %.2f%%' % percent + "\r")
        sys.stdout.flush()

    if url:
        try:
            log.debug('''
                         正在下载 %s
                         存储路径 %s
                      '''
                      % (url, file_path))

            request.urlretrieve(url, file_path, progress_callfunc)

            log.debug('''
                         下载完毕 %s
                         文件路径 %s
                      '''
                      % (url, file_path)
                      )

            call_func and call_func()
            return 1
        except Exception as e:
            log.error(e)
            return 0
    else:
        return 0


def re_sting_title(str):
    # str = re.sub("[$a-zA-Z|\!\%\[\]\,\。\?\'\"\@\.\*\&\、\:\;\$\\\|a-zA-Z$]", "", str)
    str = re.sub("[\!\%\[\]\,\。\?\'\"\@\.\*\&\、\:\;\$\\\\/]", "", str)
    return str


if __name__ == '__main__':
    MONGO_HOST = '127.0.0.1:27017'
    mongo_conn = pymongo.MongoClient(MONGO_HOST, connect=False)
    db = mongo_conn.xuanpin
    # collection = db.weibo_duanneirong
    collection = db.zhidemai_news
    user_list = collection.find({}, no_cursor_timeout=True).sort([("insert_time", -1)]).limit(1)
    count = 0
    ss = []
    for item in user_list:
        content = item["content"]
        print(content)
        regex = r'(http.:[\S]*?.(jpg|jpeg|png|gif|bmp|webp)")'
        try:
            imgs = re.findall(regex, content, re.S | re.M)
            if imgs:
                print(imgs)
                for index, i in enumerate(imgs):
                    url = i[0].replace("https", "http")
                    base_path = "/Users/admin/pworkspace/imgs/"
                    filename = "{}_{}.jpg".format(re_sting_title(item["title"][0:25]), index)
                    result = download_file(url, base_path, filename=filename, call_func='')
                    if result == 1:
                        count += 1
                        log.info(f"第{count}条下载成功了")
                        break
                    else:
                        continue
            else:
                continue
        except Exception as err:
            log.error("下载失败")
        continue
    log.info(f"总共下载成功了 {count}条")
