# 导入自动化模块
import time
from DrissionPage import ChromiumPage
import datetime
import csv
import json
import pandas as pd
 
from urllib3.filepost import writer
 
# from openpyxl import writer
 
# 创建文件对象
f = open('../data.csv', mode='w', encoding='utf-8', newline='')
# 字典写入的方法
csv_writer = csv.DictWriter(f, fieldnames=['昵称', '点赞数', '时间', '评论'])
# 写入表头
csv_writer.writeheader()
# 打开浏览器
driver = ChromiumPage()
# 监听数据包
driver.listen.start('www.douyin.com/aweme/v1/web/search/item', method='GET')
# 访问网址信息
keyword = input('请输入关键词：')
url = f'https://www.douyin.com/search/{keyword}?type=video'
print(url)
# 访问网站
driver.get(url)
 
def get_time(ctime):
    timeArray = time.localtime(ctime)
    otherStyleTime = time.strftime("%Y.%m.%d", timeArray)
    return str(otherStyleTime)
 
def save_video_info(video_data):
    minutes = video_data['video']['duration'] // 1000 // 60
    seconds = video_data['video']['duration'] // 1000 % 60
    video_dict = {
        '用户名': video_data['author']['nickname'].strip(),
        '用户uid': 'a'+ str(video_data['author']['uid']),
        '用户ID': video_data['author']['sec_uid'],
        '粉丝数量': video_data['author']['follower_count'],
        '发表时间': get_time(video_data['create_time']),
        '视频awemeid': 'a'+ video_data['aweme_id'],
        '视频url': 'https://www.douyin.com/video/' + str(video_data['aweme_id']),
        '视频描述': video_data['desc'].strip().replace('\n', ''),
        '视频时长': "{:02d}:{:02d}".format(minutes, seconds),
        '点赞数量': video_data['statistics']['digg_count'],
        '收藏数量': video_data['statistics']['collect_count'],
        '评论数量': video_data['statistics']['comment_count'],
        '下载数量': video_data['statistics']['download_count'],
        '分享数量': video_data['statistics']['share_count'],
    }
 
    print(
        f"用户名: {video_dict['用户名']}\n",
        f"用户uid: {video_dict['用户uid']}\n",
        f"用户ID: {video_dict['用户ID']}\n",
        f"粉丝数量: {video_dict['粉丝数量']}\n",
        f"发表时间: {video_dict['发表时间']}\n",
        f"视频awemeid: {video_dict['视频awemeid']}\n",
        f"视频url: {video_dict['视频url']}\n",
        f"视频描述: {video_dict['视频描述']}\n",
        f"视频时长: {video_dict['视频时长']}\n",
        f"点赞数量: {video_dict['点赞数量']}\n",
        f"收藏数量: {video_dict['收藏数量']}\n",
        f"评论数量: {video_dict['评论数量']}\n",
        f"下载数量: {video_dict['下载数量']}\n",
        f"分享数量: {video_dict['分享数量']}\n"
    )
 
    return video_dict
 
data_list1 = []
for page in range(100):
    print(f'正在采集第{page+1}页的数据内容')
    # 下滑页面到底部
    driver.scroll.to_bottom()
    # 等待数据包加载
    resp = driver.listen.wait()
    # 直接获取数据包返回的响应数据
    json_data = resp.response.body
    # print(json_data)
    # print(json.dumps(json_data, ensure_ascii=False))
    time.sleep(2)
    print(json_data['has_more'])
    data_list2 = []
    for json_aweme_info in json_data['data']:
        data = save_video_info(json_aweme_info['aweme_info'])
        data_list2.append(data)
    if json_data['has_more'] == 0:
        break
        # f = open(f'{keyword}.csv', 'a', encoding='utf-8-sig', newline="")
        # writer = csv.DictWriter(f, header)
        # writer.writeheader()
    data_list1.extend(data_list2)
    print(data_list1)
 
# 向csv文件写入表头，评论数据csv文件
header = ['用户名',
          '用户uid',
          '用户ID',
          '粉丝数量',
          '发表时间',
          '视频awemeid',
          '视频url',
          '视频描述',
          '视频时长',
          '点赞数量',
          '收藏数量',
          '评论数量',
          '下载数量',
          '分享数量']
 
today_indx = datetime.date.today()
 
df = pd.DataFrame(data=data_list1, columns=header )
# print(df)
 
df.to_excel(f'{keyword}-{today_indx}.xlsx',index=False)