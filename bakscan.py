# -*- coding: utf-8 -*-
# @Author: mrwu
# @Date:   2022-03-07 09:43:19
# @Last Modified by:   mrwu
# @Last Modified time: 2022-07-01 17:47:44

from multiprocessing import Pool
from tqdm import tqdm
import requests
import re
import argparse
requests.packages.urllib3.disable_warnings()  #关闭ssl控制台报错

header = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
## inurl 定义要扫的备份文件
inurl = {"/www.zip","/www.rar","/www.tar.gz","/www.gz","/wwwroot.zip","/wwwroot.rar","/wwwroot.tar.gz","/wwwroot.gz","/web.zip","/web.rar","/web.tar.gz","/web.gz","/七月修复weipan.zip","/weipan.zip","/weipan.rar","/weipan.tar.gz"}
hz = {".zip",".rar",".tar.gz"}

urllist = []

def banner():
    print('''  ____             _                       _____                 
 |  _ \           | |                     / ____|                
 | |_) | __ _  ___| | ___   _ _ __  ___  | (___   ___ __ _ _ __  
 |  _ < / _` |/ __| |/ / | | | '_ \/ __|  \___ \ / __/ _` | '_ \ 
 | |_) | (_| | (__|   <| |_| | |_) \__ \  ____) | (_| (_| | | | |
 |____/ \__,_|\___|_|\_\\__,_| .__/|___/ |_____/ \___\__,_|_| |_|
                             | |                                 
                             |_|                                 

 Author:MrWu           Blog:www.mrwu.red        
                                               ''')

def save(data):
    f = open(r'fail_url.txt', 'a',encoding='utf-8')
    f.write(data + '\n')
    f.close()

def open_url(url):
    with open(url) as f:
        for url in f:
            url = url.replace("\n","").split()
            for x in url:
                for index in hz:
                    if x.startswith("https://"):
                        url1 = x + '/' + x.replace("https://","") + index
                    if x.startswith("http://"):
                        url1 = x + '/' + x.replace("http://","") + index
                    urllist.append(url1)
                for s in list(inurl):
                    url = x + s
                    urllist.append(url)
    return(urllist)

def run(url):
    try:
        html = requests.get(url, headers=header,verify=False,timeout=(2,2))
        html.encoding = 'utf-8'
        code = html.status_code
        html = html.headers['Content-Type']
        result = "application" in html 
        result2 = "application/json" in html
        if result == True and result2 == False:
            print('\033[1;31m[!] 目标：%s ----- 文件存在 ----- 状态码：%s\033[0m'%(url,code))
    except Exception as e:
        save(url)

if __name__ == '__main__':
    banner()

    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url', default='url.txt',help="URL文件路径")
    parser.add_argument('-t','--threads', default='60',help="进程数，不要超过60")
    args = parser.parse_args()

    urllist = open_url(args.url)
    po = Pool(int(args.threads)) #最高60
    #进度条显示
    pbar = tqdm(total=len(urllist))
    pbar.set_description('正在扫描')
    update = lambda *args: pbar.update()
    #进度条显示
    for url in urllist:
        po.apply_async(run,(url,), callback=update)
    po.close()
    po.join()