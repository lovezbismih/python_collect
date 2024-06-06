import concurrent.futures
import importlib
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
 
import rarfile
import requests
from bs4 import BeautifulSoup
 
 
def download(url, category, level, name):
    path = category + "/" + level + "/" + name + ".rar"
    dir_name = os.path.dirname(path)
    os.makedirs(dir_name, exist_ok=True)
    res = requests.get(domain + url, headers=dic)
    with open(path, "wb") as f:
        f.write(res.content)
        f.flush()
        print(f'线程:{threading.current_thread().name} 下载完成:{path}')
    # 解压
    extract_rar(path, category + "/" + level)
    # 自动删除rar
    os.remove(path)
 
 
def extract_rar(file_path, extract_path):
    with rarfile.RarFile(file_path) as rf:
        for member in rf.infolist():
            if not member.filename.endswith('.doc'):
                continue
            rf.extract(member.filename, extract_path)
 
 
def get_page_list(page_url):
    root = requests.get(domain + page_url, headers=dic)
    root.encoding = "gb2312"
    root_html = BeautifulSoup(root.text, "html.parser")
    tr_list = root_html.find("div", class_="listbox").find("table").find_all("tr")
    for index, tr in enumerate(tr_list):
        if index == 0 or (tr.text.find(".doc") == -1):
            continue
        tds = tr.find_all("td")
        name = tds[0].text
        suffix = tds[1].text
        level = tds[2].text
        category = tds[3].text
        child_url = domain + tds[0].find("a").get("href")
        child_html = BeautifulSoup(requests.get(child_url, headers=dic).text, "html.parser")
        a = child_html.find("div", class_="content").find_next("a")
        down_url = a.get("href")
        print(f'开始下载:{category}-{level}-{name}{suffix} url: {domain}{down_url}')
        task = pool.submit(download, down_url, category, level, name)
        task_list.append(task)
 
    # 返回下一页的url
    pages = root_html.find("div", class_="dede_pages").find("ul").find_all("li")
    stop = False
    for i in pages:
        if stop:
            return i.find("a").get("href")
        cls: list[str] = i.get("class")
        if cls and "thisclass" in cls:
            stop = True
    return None
 
 
# 环境检测
def pip_install():
    print("正在检测安装依赖...")
    paks = ["rarfile", "requests", "beautifulsoup4"]
    name = ""
    try:
        for pak in paks:
            name = pak
            importlib.import_module(name)
    except ImportError:
        print(f"依赖未安装[{name}],开始安装 ========> pip install {name}")
        subprocess.check_call(["pip", "install", name])
 
    winrar: bool = os.path.exists("C:\\Windows\\UnRAR.exe")
    if not winrar:
        print("请安装winrar解压缩软件,并将UnRAR.exe复制到【C:\\Windows】目录.")
        sys.exit()
    print("依赖安装完成")
 
 
maps: dict = {}
menus: dict = {}
 
 
def request_menus():
    home = requests.get(domain, headers=dic)
    home.encoding = "gb2312"
    home_html = BeautifulSoup(home.text, "html.parser")
    uls = home_html.find("div", class_="linkbox").find_all("ul")
    num = 1
    for ul in uls:
        lis = ul.find_all("li")
        key = lis[0].find("font").text
        objs = []
        for i in range(1, len(lis)):
            a = lis[i].find("a").get("href")
            font = lis[i].find("a").text
            obj = {
                "num": num,
                "a": a,
                "font": font
            }
            maps[str(num)] = a
            objs.append(obj)
            num = num + 1
        menus[key] = objs
 
 
def print_menus():
    print("数据来源：第一试卷网(www.shijuan1.com) 商务合作：shijuan2011@163.com 仅支持个人研究和学习,商用请联系官方授权.\n")
    for key, value in menus.items():
        text = ''
        for obj in value:
            text += f'({obj.get("num")}){obj.get("font")} '
        print(f'{key} : {text}')
 
 
def select_menus() -> str:
    if not menus:
        request_menus()
 
    print_menus()
    sc = input("请输入序号开始下载：\n")
    while not maps.get(sc):
        sc = input("输入错误,请重新输入：\n")
 
    return maps.get(sc)
 
 
if __name__ == '__main__':
    print("声明:本代码仅供学习研究使用,请勿用于商业用途,否则后果自负!")
    print("声明:本代码仅供学习研究使用,请勿用于商业用途,否则后果自负!")
    print("声明:本代码仅供学习研究使用,请勿用于商业用途,否则后果自负!")
    pip_install()
    domain = "https://www.shijuan1.com/"
    dic = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    print("声明:本代码仅供学习研究使用,请勿用于商业用途,否则后果自负!")
    # 创建线程池
    pool = ThreadPoolExecutor(5)
    task_list = []
    # 打印菜单,等待输入
    url: str = select_menus()
 
    # 开始下载
    next_page = url + get_page_list(url)
    # 等待所有任务完成
    concurrent.futures.wait(task_list, return_when='ALL_COMPLETED')
 
    while next_page:
        print(f'开始下载下一页:{next_page}, 请稍等...')
        time.sleep(60)
        next_page = url + get_page_list(next_page)
 
    pool.shutdown()
    print("所有任务完成,共下载{}个文件", len(task_list))
 
    # 打印菜单
    select_menus()