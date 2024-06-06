import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import requests
import os
 
def download_content():
    # 获取用户输入的URL
    url = url_entry.get()
    if not url:
        messagebox.showerror("错误", "请输入网址")
        return
 
    # 获取保存路径
    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showerror("错误", "请选择保存路径")
        return
 
    # 确保保存路径存在
    os.makedirs(save_path, exist_ok=True)
 
    # 使用requests获取网页内容
    response = requests.get(url)
 
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
 
        # 提取文本内容
        paragraphs = soup.find_all('p')
        text_list = [p.get_text() for p in paragraphs]
 
        # 合并文本
        merged_text = '\n'.join(text_list)
 
        # 获取网页标题
        title = soup.title.string.strip() if soup.title else 'default_title'
 
        # 保存文本到文件
        with open(os.path.join(save_path, f'{title}.txt'), 'w', encoding='utf-8') as file:
            file.write(merged_text)
 
        print('文本已保存')
 
        # 设置浏览器选项
        myoption = webdriver.ChromeOptions()
        myoption.add_experimental_option("excludeSwitches", ["enable-automation"])
        myoption.add_experimental_option('useAutomationExtension', False)
        myoption.add_argument("--headless")  # 无界面浏览
        wd = webdriver.Chrome(service=Service(r'D:\chrome\chrome-win64\chromedriver.exe'), options=myoption)
        wd.maximize_window()
        wd.implicitly_wait(10)
 
        # 获取图片地址并下载
        wd.get(url)
        pic = wd.find_elements(By.XPATH, '//img[@data-src]')
        num = len(pic)
        for num_i in range(num):
            pic_url = pic[num_i].get_attribute("data-src")
            response = requests.get(pic_url)
            mingcheng = title + str(num_i)
            with open(os.path.join(save_path, f'image_{mingcheng}.jpg'), 'wb') as f:
                f.write(response.content)
            print('正在下载第: ' + str(num_i) + '张图片')
            sleep(0.5)
 
        # 关闭浏览器
        wd.quit()
 
        messagebox.showinfo("成功", "文本和图片已保存")
    else:
        messagebox.showerror("错误", f'请求失败，状态码：{response.status_code}')
 
# 创建主窗口
root = tk.Tk()
root.title("网页内容下载器")
 
# 创建并放置控件
tk.Label(root, text="请输入网址:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)
 
download_button = tk.Button(root, text="下载内容", command=download_content)
download_button.grid(row=1, columnspan=2, pady=10)
 
# 运行主循环
root.mainloop()