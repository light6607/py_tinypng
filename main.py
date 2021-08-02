import requests
import random
import time
import argparse
import os
import typing
from utils.func_time import clock


# https://docs.python.org/zh-cn/3/library/argparse.html

def generate_ip() -> str:
    address_8 = random.randint(0, 255)
    address_16 = random.randint(0, 255)
    address_24 = random.randint(0, 255)
    address_32 = random.randint(0, 255)
    random_ip = f'{address_8}.{address_16}.{address_24}.{address_32}'
    return random_ip


@clock(msg='compress picture')
def compress_png(in_file: str, out_file: str) -> typing.NoReturn:
    headers = {
        "X-Forwarded-For": generate_ip(),
        'Postman-Token': str(int(time.time() * 1000)),
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }
    with open(in_file, 'rb') as f:
        data = f.read()
    r = requests.post(url='https://tinypng.com/web/shrink', headers=headers, data=data)
    res_info = r.json()
    origin_size = res_info['input']['size'] / 1024
    output_size = res_info['output']['size'] / 1024
    compress_percent = round((1 - output_size / origin_size) * 100, 2)
    output_url = res_info['output']['url']

    r = requests.get(url=output_url)
    with open(out_file, 'wb') as f:
        f.write(r.content)
    print(
        f'*** {in_file} origin_size:{origin_size} KB output_size:{output_size} KB compress percent:{compress_percent}%  out:{out_file}***')


@clock(msg='主函数执行耗时')
def main():
    parser = argparse.ArgumentParser(description='Please input your input folder and output folder')
    parser.add_argument('input', help='folder of origin pictures')
    parser.add_argument('output', help='folder to output pictures')
    args = parser.parse_args()
    print(f'your input folder is {args.input}, and output folder is {args.output}')
    # for test
    # in_path = "./origin_png"
    # out_path = "./output"
    in_path = args.input
    out_path = args.output
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    file_list = os.listdir(in_path)
    for filename in file_list:
        compress_png(in_file=f'{in_path}/{filename}', out_file=f'{out_path}/{filename}')


if __name__ == '__main__':
    main()
