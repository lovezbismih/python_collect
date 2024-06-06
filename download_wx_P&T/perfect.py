import ctypes
import subprocess
import sys
import os
import random
import re
import uuid
import shutil
import datetime
import requests
import secrets
from bs4 import BeautifulSoup
from qiniu import Auth, put_file, BucketManager, urlsafe_base64_encode
import qiniu.config
import mimetypes
import pyperclip
from datetime import datetime as dt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QSettings, QSize, QPoint, pyqtSignal, QThread
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
 
# 隐藏命令行窗口
def hide_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
 
# 设置窗口位置和大小
def set_console_position_and_size(left, top, width, height):
    # 获取控制台窗口句柄
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
 
    if hwnd:
        # 调用 MoveWindow 函数来设置窗口位置和大小
        ctypes.windll.user32.MoveWindow(hwnd, left, top, width, height, True)
 
# 设置窗口位置 (左, 上) 和大小 (宽度, 高度)
left = -7
top = 1506
width = 335
height = 200
 
# 设置命令行窗口的大小和位置
set_console_position_and_size(left, top, width, height)
 
# 七牛云配置信息
access_key = '手动填写'
secret_key = '手动填写'
bucket_name = '手动填写'
domain = '手动填写'
pipeline = 'default.sys'
key = 'l/tupian/'
fops = 'imageView2/0/interlace/1/q/90|imageslim'
uploaded_images = {}  # 用于存储已经上传过的图片
 
q = Auth(access_key, secret_key)
bucket = BucketManager(q)
policy = {'persistentPipeline': pipeline}
 
if os.path.exists('.qiniu_pythonsdk_hostscache.json'):
    os.remove('.qiniu_pythonsdk_hostscache.json')
 
class FetchImagesThread(QThread):
    progress_signal = pyqtSignal(str)
 
    def __init__(self, url):
        super().__init__()
        self.url = url
 
    def run(self):
        self.fetch_images_from_url(self.url)
 
    def fetch_images_from_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'id': 'js_content'})
 
        if not os.path.exists('D:\\临时图片'):
            os.makedirs('D:\\临时图片')
 
        img_re = re.compile(r'<img [^<>]*src=["\']?([^"\'>]+)["\']?[^<>]*>')
        img_list = img_re.findall(str(content))
 
        bg_img_re = re.compile(r'background-image:\s*url\(["\']?([^"\'>]+)["\']?\)')
        bg_img_list = bg_img_re.findall(str(content))
 
        img_list.extend(bg_img_list)
 
        for index, img_url in enumerate(img_list):
            if img_url in uploaded_images:
                img_new_url = uploaded_images[img_url]
            else:
                response = requests.head(img_url)
                content_type = response.headers.get('content-type')
                img_type = content_type.split('/')[-1]
 
                if img_type == 'jpeg':
                    img_ext = '.jpg'
                elif img_type == 'png':
                    img_ext = '.png'
                elif img_type == 'gif':
                    img_ext = '.gif'
                elif img_type == 'svg+xml':
                    img_ext = '.svg'
                else:
                    img_ext = '.jpg'
 
                new_img_url = re.sub(r'\.\w+$', img_ext, img_url)
 
                img_data = requests.get(new_img_url).content
                img_name = f"D:\\临时图片\\{secrets.token_hex(4)}{img_ext}"
                with open(img_name, 'wb') as f:
                    f.write(img_data)
 
                today = datetime.datetime.now().strftime('%Y/%m-%d')
                title = url.split('/')[-1].split('.')[0]
                img_key = f"{key}{today}/{title}/{secrets.token_hex(4)}{img_ext}"
                token = q.upload_token(bucket_name, img_key)
                ret, info = put_file(token, img_key, img_name, check_crc=True)
 
                img_new_url = f"{domain}/{img_key}"
                uploaded_images[img_url] = img_new_url
 
            content = re.sub(r'src=["\']?' + re.escape(img_url) + r'["\']?', f'src="{img_new_url}"', str(content))
            content = re.sub(r'background-image:\s*url\(["\']?' + re.escape(img_url) + r'["\']?\)', f'background-image: url("{img_new_url}")', str(content))
 
            self.progress_signal.emit(f"替换后的链接: {img_new_url}")
 
        content = re.sub(r'data-src', 'src', content)
 
        timestamp = datetime.datetime.now().strftime('%H.%M.%S')
        file_name = f"C:/Users/Administrator/Desktop/采集_{timestamp}.html"
        with open(file_name, 'w', encoding='utf-8') as f:
            # 删除生成的无用代码段
            cleaned_content = re.sub(r'style="display: none;"', '', str(content))
            f.write(cleaned_content)
             
        self.progress_signal.emit(f"文件已保存至：{file_name}")
        shutil.rmtree('D:\\临时图片')
        self.progress_signal.emit("下载的文件已删除")
 
        if os.path.exists('.qiniu_pythonsdk_hostscache.json'):
            os.remove('.qiniu_pythonsdk_hostscache.json')
 
class DragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
 
        self.init_ui()
        self.setAcceptDrops(True)
        self.last_file_is_video = False
 
        # 设置窗口位置到左下角
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.left(), screen.bottom() - self.height() - 276)
 
        # 读取上次保存的窗口位置和大小
        settings = QSettings('MyApp', 'DragDropWidget')
        self.resize(settings.value('size', QSize(400, 300)))
        self.move(settings.value('pos', QPoint(300, 300)))
 
    def init_ui(self):
        self.setWindowTitle('图片+视频+公众号采集')
        self.setGeometry(300, 300, 400, 300)  # 窗口大小设置为400x300
 
        layout = QVBoxLayout()
 
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('请输入公众号文章的链接')
        layout.addWidget(self.url_input)
 
        self.fetch_button = QPushButton('点击采集', self)
        self.fetch_button.clicked.connect(self.fetch_images)
        layout.addWidget(self.fetch_button)
 
        self.label = QLabel('请拖拽文件或文件夹到此窗口进行上传', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
 
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
 
        self.progress_text = QTextEdit(self)
        self.progress_text.setReadOnly(True)
        layout.addWidget(self.progress_text)
 
        self.size_label = QLabel('当前默认尺寸：宽1200px', self)
        self.size_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.size_label)
 
        button_layout = QHBoxLayout()
        self.button_1200px = QPushButton('宽1200px', self)
        self.button_1200px.clicked.connect(lambda: self.set_size_option('1200px'))
        self.button_original = QPushButton('原始尺寸', self)
        self.button_original.clicked.connect(lambda: self.set_size_option('原始尺寸'))
        button_layout.addWidget(self.button_1200px)
        button_layout.addWidget(self.button_original)
 
        layout.addLayout(button_layout)
        self.setLayout(layout)
 
        self.size_option = '1200px'
 
    def fetch_images(self):
        url = self.url_input.text().strip()
        if url:
            self.progress_text.append("开始采集图片...")
            self.thread = FetchImagesThread(url)
            self.thread.progress_signal.connect(self.update_progress)
            self.thread.start()
 
    def set_size_option(self, option):
        self.size_option = option
        self.size_label.setText(f'当前选择：{option}')
        if option == '1200px':
            self.button_1200px.setStyleSheet('background-color: lightblue')
            self.button_original.setStyleSheet('')
        else:
            self.button_original.setStyleSheet('background-color: lightblue')
            self.button_1200px.setStyleSheet('')
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
 
    def dropEvent(self, event):
        uploaded_files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            mime_type, _ = mimetypes.guess_type(file_path)
 
            if os.path.isdir(file_path):
                # 如果是文件夹，遍历文件夹内所有文件并上传
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        result = self.upload_file_or_video(file_path)
                        if result:
                            uploaded_files.append(result)
            else:
                # 如果是文件，直接上传
                result = self.upload_file_or_video(file_path)
                if result:
                    uploaded_files.append(result)
 
        if uploaded_files:
            self.result_label.setText(f'上传成功，共上传 {len(uploaded_files)} 个文件')
            self.generate_html(uploaded_files)
        else:
            self.result_label.setText('上传失败，请重试')
 
    def upload_file_or_video(self, file_path):
        key_prefix = 'l/tupian/' if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) else 'l/shipin/'
 
        key = key_prefix + dt.now().strftime('%Y/%m-%d') + '/' + str(random.randint(10000000, 99999999)) + os.path.basename(file_path)
        saveas_key = urlsafe_base64_encode(f'{bucket_name}:{key}')
 
        if key_prefix == 'l/tupian/':
            fops = 'imageView2/0/interlace/1/q/90|imageslim|saveas/' + saveas_key
        else:
            fops = 'vframe/jpg/offset/0.1/saveas/' + saveas_key
 
        policy['persistentOps'] = fops
        token = q.upload_token(bucket_name, key, 3600, policy=policy)
        ret, info = put_file(token, key, file_path, version='v2')
 
        if info.status_code == 200:
            self.update_progress(f'{key} {"图片" if key_prefix == "l/tupian/" else "视频"}上传成功')
            return f'{domain}/{key}'
 
        return None
 
    def generate_html(self, uploaded_files):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") 
        html_path = os.path.join(desktop_path, 'uploaded_files.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write('<style style="text-align: center;"></style><p>')
            for i, file in enumerate(uploaded_files):
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    if self.size_option == '1200px':
                        f.write(f'<img src="{file}" style="width: 1200px;"/>')
                    else:
                        f.write(f'<img src="{file}" style="width: auto;"/>')
                elif file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    if not self.last_file_is_video:
                        f.write(f'<video poster="{file}?vframe/jpg/offset/0.1" src="{file}" controls="controls" style="width:100%; height:100%;" autoplay="autoplay" webkit-playsinline="true" playsinline="true" x5-playsinline="true"></video></p>')  
                    # Copy the video code to the clipboard
                    pyperclip.copy(f'<p><video poster="{file}?vframe/jpg/offset/0.1" src="{file}" controls="controls" style="width:100%; height:100%;" autoplay="autoplay" webkit-playsinline="true" playsinline="true" x5-playsinline="true"></video></p>')
                    self.last_file_is_video = True
 
        self.update_progress(f'已生成HTML文件:{html_path}')
        if os.path.exists('.qiniu_pythonsdk_hostscache.json'):
            os.remove('.qiniu_pythonsdk_hostscache.json')
 
    def update_progress(self, message):
        self.progress_text.append(message)
 
    def closeEvent(self, event):
        # 保存窗口位置和大小
        settings = QSettings('MyApp', 'DragDropWidget')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        event.accept()
 
if __name__ == '__main__':
    hide_console()
    app = QApplication(sys.argv)
    widget = DragDropWidget()
    widget.show()
    sys.exit(app.exec_())