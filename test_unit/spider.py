# 爬取一些资源存储到../origin_png/ 用于做压缩测试
import requests
import time
import typing
import os
from utils.func_time import clock


@clock('拉取壁纸图片')
def get_network_img(category: str, req_num: int, folder: str) -> typing.NoReturn:
    req = requests.get(
        url=f'http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category={category}&tag=%E5%85%A8%E9%83%A8&start=0&len={req_num}')
    img_dict = req.json()
    img_url_list = []
    for img_tiem in img_dict['all_items']:
        img_url_list.append(img_tiem['bthumbUrl'])

    for index, img_url in enumerate(img_url_list):
        start_time = time.time()
        r = requests.get(url=img_url, timeout=10)
        filename = f'{folder}/{index}.png'
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f'***download {img_url} to file: {filename} over ,use {time.time() - start_time} seconds ***')


if __name__ == '__main__':
    if not os.path.exists('../origin_png'):
        os.makedirs('../origin_png')
    get_network_img(category='壁纸', req_num=10, folder='../origin_png/')
