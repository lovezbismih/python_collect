# 使用request模块去发送请求
# 发送请求
# 需要js逆向：加密参数a_bogus
# 获取数据
# 解析数据
# 保存数据
 
# 使用DrissionPage
# 打开浏览器
# 访问网站
# 监听数据包，获取响应数据
# 解析数据
# 保存数据
 
# 导入自动化模块
from DrissionPage import ChromiumPage
import datetime
import csv
import json
 
# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
# 字典写入的方法
csv_writer = csv.DictWriter(f, fieldnames=['昵称', '点赞数', '时间', '评论'])
# 写入表头
csv_writer.writeheader()
# 打开浏览器
driver = ChromiumPage()
# 监听数据包
driver.listen.start('aweme/v1/web/comment/list/')
# 访问网站
driver.get('https://www.douyin.com/video/7349362406147001610')
for page in range(30):
    print(f'正在采集第{page+1}页的数据内容')
    # 下滑页面到底部
    driver.scroll.to_bottom()
    # 等待数据包加载
    resp = driver.listen.wait()
    # 直接获取数据包返回的响应数据
    json_data = resp.response.body
    # print(json.dumps(json_data))
    # 解析数据，提取评论数据所在的列表
    comments = json_data['comments']
    # for 循环变量，提取列表里面的元素
    for index in comments:
        # 键值对取值，提取相关内容
        text = index['text']  #评论内容
        nickname = index['user']['nickname']    # 昵称
        create_time = index['create_time'] #创建时间
        # 把时间戳转换成日期
        create_time = str(datetime.datetime.fromtimestamp(create_time))
        digg_count = index['digg_count']
        # 把数据放在字典里面
        dict = {
            '昵称': nickname,
            '点赞数': digg_count,
            '时间': create_time,
            '评论': text,
        }
 
        # 写入数据
        csv_writer.writerow(dict)
        print(dict)