import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
 
# 设置Chrome选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
 
# 初始化webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
 
# 假设txt文件名为"urls.txt"，并且位于当前工作目录中
txt_file_path = "{.txt"
 
# 读取txt文件中的内容
with open(txt_file_path, 'r', encoding='utf-8') as file:
    content = file.read()
 
# 解析JSON内容
urls = json.loads(content)
urls1 = urls["url"]
 
# 创建一个主文件夹来保存所有下载的图片
os.makedirs('downloaded_images', exist_ok=True)
 
# 遍历URL列表，下载每个网页上的所有图片
for idx, url in enumerate(urls1):
    print(f"正在处理URL {idx+1}: {url}")
    driver.get(url)
     
    # 模拟缓慢滚动行为
    SCROLL_PAUSE_TIME = 0.1
    scroll_increment = 500
 
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
 
    while current_position < last_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        current_position += scroll_increment
        time.sleep(SCROLL_PAUSE_TIME)
        last_height = driver.execute_script("return document.body.scrollHeight")
 
    # 确保已滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    images = soup.find_all('img')  # 查找指定类名的图片 , class_='rich_pages wxw-img'
 
    # 为每个URL创建一个独立的文件夹
    folder_name = f"url_{idx+1}"
    folder_path = os.path.join('downloaded_images', folder_name)
    os.makedirs(folder_path, exist_ok=True)
 
    for img_idx, img in enumerate(images):
        img_url = img.get('data-src')
        if not img_url:
            img_url = img.get('src')  # 尝试获取src属性
 
        if img_url and not img_url.startswith('data:'):
            # 检查URL是否完整
            if not img_url.startswith(('http:', 'https:')):
                img_url = requests.compat.urljoin(url, img_url)
 
            # 获取图片内容的响应
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # 按顺序命名图片
                img_name = f"{img_idx+1}.png"
                img_path = os.path.join(folder_path, img_name)
 
                # 保存图片
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                    print(f"图片已下载: {img_path}")
            else:
                print(f"无法下载图片: {img_url}")
        else:
            print(f"无效的图片URL: {img_url}")
 
driver.quit()
print("所有图片下载完成。")