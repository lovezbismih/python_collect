import concurrent.futures
import os
import threading
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
 
 
def getPageList(page_index):
    page_url = f"a/sjyw4/list_109_{page_index}.html"
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
 
 
if __name__ == '__main__':
    domain = "https://www.shijuan1.com/"
    dic = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    # 创建线程池
    pool = ThreadPoolExecutor(5)
    task_list = []
 
    # 遍历10页,下载
    for page in range(1, 10):
        getPageList(page)
 
    # 等待所有任务完成
    concurrent.futures.wait(task_list, return_when='ALL_COMPLETED')
    pool.shutdown()
    print("所有任务完成,共下载{}个文件", len(task_list))