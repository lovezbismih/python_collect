# -*- coding:UTF-8 -*-
 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import requests
 
 
myoption = webdriver.ChromeOptions()
myoption.add_experimental_option("excludeSwitches", ["enable-automation"])
myoption.add_experimental_option('useAutomationExtension', False)
myoption.add_argument("--headless")  # 无界面浏览
wd = webdriver.Chrome(service=Service(r'D:\chrome\chrome-win64\chromedriver.exe'), options=myoption)
wd.maximize_window()
wd.implicitly_wait(10)
 
url = input('输入网址：')
wd.get(url)
 
# 获取文本
span = wd.find_elements(By.XPATH, '//span[@style]')
title = wd.find_element(By.CLASS_NAME, 'rich_media_title').text
text_list = []
for text in span:
    span_text = f"{text.text}"
    text_list.append(span_text)
 
liebiao_text = text_list
 
merged_text = ''.join(liebiao_text)
new_merged_text = merged_text.replace('。', '\n')
 
# 打开文件
file = open('path/to/save/' + title + '.txt', "w", encoding='utf-8')
 
# 写入数据
file.write(new_merged_text)
 
# 关闭文件
file.close()
 
# 获取图片地址
pic = wd.find_elements(By.XPATH, '//img[@data-src]')
num = len(pic)
for num_i in range(num):
    # print(num_i)
    pic_url = pic[num_i].get_attribute("data-src")
    response = requests.get(pic_url)
    mingcheng = title + str(num_i)
    with open('path/to/save/image_' + mingcheng + '.jpg', 'wb') as f:
        # 写入获取到的内容
        f.write(response.content)
    print('正在下载第: ' + str(num_i) + '张图片')
    sleep(0.5)