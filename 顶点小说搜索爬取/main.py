import asyncio
import os.path
import aiohttp
import aiofiles
import requests
from lxml import etree
from urllib.parse import urljoin
 
# 小说下载器，基于异步IO和aiohttp库  用于合成网址
main_url = 'https://www.23wxx.cc/'
 
 
async def download(down_url, file_name):
    """
    异步下载小说章节并保存到文件。
 
    :param down_url: 章节内容的URL
    :param file_name: 保存章节内容的文件名（包含路径）
    """
    headers = {
        # 翻页的cookie需要从随便一个翻页获取
        'Cookie': 'waf_sc=5889647726; novel_3341=1254203%7C1715791397; novel_5992=894457%7C1715795498; Hm_lvt_214c2a461550c6e33904c2abd04c890a=1715787170,1715819564; novel_5177=966743%7C1715821321; Hm_lpvt_214c2a461550c6e33904c2abd04c890a=1715821317',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'Referer': down_url
    }
 
    for i in range(5):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(down_url, headers=headers) as response:
 
                    content = await response.text(encoding='utf-8',errors='ignore')
                    # content.decode('utf-8', errors='ignore')  # 忽略错误字节
                    # 获取响应的Cookie
                    response_cookies = response.cookies
                    # 更新Cookie 否则有下一页会下载失败
                    cookie_str = "; ".join([f"{key}={value.value}" for key, value in response_cookies.items()])
                    headers['Cookie'] = cookie_str
 
                    tree = etree.HTML(content)
                    texts = tree.xpath('//div[@id="content"]/p//text()')[:-1]
                    next_characters = tree.xpath('//a[@id="A3"]//text()')[0]
                    if next_characters:
                        next_url = urljoin(main_url, tree.xpath('//a[@id="A3"]//@href')[0])
 
                    texts = ''.join(texts)
 
                    async with aiofiles.open(file_name, 'w', encoding='utf-8') as f:
                        await f.write(file_name+'\n'+texts)
            if next_characters != '下一页':
                break
            while next_characters == '下一页':
                """
                如果存在下一页，则继续下载。
                """
                down_url = next_url
 
                async with aiohttp.ClientSession() as session:
                    async with session.get(down_url, headers=headers) as response:
                        content = await response.text(encoding='utf-8', errors='ignore')
                        # print(response.url)
                        tree = etree.HTML(content)
                        texts = tree.xpath('//div[@id="content"]/p//text()')[:-1]
                        next_characters = tree.xpath('//a[@id="A3"]//text()')[0]
 
                        if next_characters:
                            next_url = urljoin(main_url, tree.xpath('//a[@id="A3"]//@href')[0])
 
                        texts = ''.join(texts)
                        async with aiofiles.open(file_name, 'a', encoding='utf-8') as f:
                            await f.write(texts)
 
            print(f'{file_name}下载完成')
            break
        except Exception as e:
            print(f'{file_name}下载失败,正在重新下载：{e}')
 
 
async def main(lst_info, name):
    """
    主函数，用于处理小说的下载任务。
 
    :param lst_info: 包含小说章节信息的列表
    :param name: 小说名称，用于保存文件
    """
    if not os.path.exists(name):
        os.makedirs(name)
    num = 1
    tasks = []
    for info in lst_info[:]:
        down_url = info['chapter_url']
        chapter_name = info['chapter_name']
        file_name = f'{name}/{num:04}-{chapter_name}.txt'
        file_name = file_name.replace(' ', '').strip().replace('*', '')  # * 号不能用于文件名 避免报错
        num += 1
        tasks.append(asyncio.create_task(download(down_url, file_name)))
    await asyncio.gather(*tasks)
 
 
def main_search():
    while True:
        url = 'https://www.23wxx.cc/search.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
            'Cookie': 'waf_sc=5889647726; Hm_lvt_214c2a461550c6e33904c2abd04c890a=1715787170; Hm_lpvt_214c2a461550c6e33904c2abd04c890a=1715787479',
            'Referer': 'https://www.23wxx.cc/search/804/1.html'
        }
        # 用户输入小说名称，输入q退出
        name = input('请输入小说名,输入q退出：')
        if name == 'q':
            break
        else:
            # 发送POST请求搜索小说
            data = {
                'searchtype': 'all',
                'searchkey': name
            }
            res = requests.post(url, data=data, headers=headers)
 
            # 更新Referer为搜索结果页面的URL
            # headers['Referer'] = str(res.url)
 
            # 解析搜索结果页面
            tree = etree.HTML(res.text)
            dls = tree.xpath('//div[//div[@id="sitembox"]]/dl')
            if len(dls) == 0:
                print('没有找到小说')
                continue
            else:
                # 打印搜索到的小说信息
                lst = []
                num = 1
                for dl in dls:
                    title = dl.xpath('./dd[1]//a//text()')[0]
                    info = dl.xpath('./dd[2]//text()')
                    info = ' '.join(info).strip()
                    url = dl.xpath('./dd[1]//a/@href')[0]
                    url = urljoin(main_url, url)
                    print(num, title, info)
                    lst_info = [title, url]
                    lst.append(lst_info[:])
                    num += 1
 
                # 用户输入要下载的小说序号
                num = input('请输入你想下载的小说序号：')
                if num.isdigit() and 0 < int(num) <= len(lst):
                    # 发送GET请求获取小说详情页面
                    resp = requests.get(lst[int(num) - 1][1], headers=headers)
                    headers['Referer'] = str(resp.url)
                    # 解析小说详情页面，获取章节信息
                    tree_child = etree.HTML(resp.text)
                    dds = tree_child.xpath('//div[@id="list"]/dl/dd')
                    new_lst_info = []
                    new_title = lst[int(num) - 1][0].strip().replace(' ', '')
                    # print(new_title)
                    for dd in dds[12:]:
                        chapter_name = dd.xpath('./a//text()')[0].replace(' ', '-')
                        chapter_url = dd.xpath('./a/@href')[0]
                        chapter_url = urljoin(main_url, chapter_url)
                        chapter_url = chapter_url.replace('.html ', '_1.html')
                        dict = {
                            'chapter_name': chapter_name,
                            'chapter_url': chapter_url
                        }
                        new_lst_info.append(dict)
 
                    # 下载小说章节
                    # now = time.time()
                    asyncio.run(main(new_lst_info, new_title))
                    # print('下载完成', time.time() - now)
                    if not os.path.exists(new_title):
                        print("文件不存在")
                    else:
                        list_path = os.listdir(new_title)
                        print(list_path)
                        with open(new_title + "/" + f"{new_title}.txt", "w", encoding="utf-8") as f:
                            for i in list_path:
                                with open(new_title + "/" + i, "r", encoding="utf-8") as f1:
                                    f.write(f1.read() + '\n')
                        print(f"{new_title}合并完成")
 
 
if __name__ == '__main__':
    # 小说搜索和下载器
    # 该程序循环搜索指定小说名称，并下载用户选择的小说章节
    main_search()