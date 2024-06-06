import sys
import json
import os
import re  # 导入正则表达式模块
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QCheckBox, QTextBrowser, QMessageBox, QFileDialog, QDialog, QTextEdit
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt, QDateTime
from threading import Thread
import importlib.util
import speech_recognition as sr
import pyttsx3
import markdown
 
class AddModelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('添加模型')
        self.setGeometry(200, 200, 600, 400)
 
        main_layout = QVBoxLayout()
 
        code_label = QLabel('请输入模型代码:')
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText('在这里输入Python代码...')
        main_layout.addWidget(code_label)
        main_layout.addWidget(self.code_editor)
 
        button_layout = QHBoxLayout()
        self.save_button = QPushButton('保存')
        self.save_button.clicked.connect(self.save_model)
        button_layout.addWidget(self.save_button)
 
        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)
 
        main_layout.addLayout(button_layout)
 
        self.setLayout(main_layout)
 
    def save_model(self):
        model_code = self.code_editor.toPlainText()
        if model_code.strip():
            # 获取主模块文件的路径
            main_module_path = sys.modules['__main__'].__file__
            main_module_dir = os.path.dirname(main_module_path)
            file_path, _ = QFileDialog.getSaveFileName(self, "保存模型", main_module_dir, "Python文件 (*.py);;All Files (*)")
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(model_code)
                QMessageBox.information(self, "提示", "模型已成功保存！")
                self.close()
        else:
            QMessageBox.warning(self, "警告", "请输入模型代码！")
 
 
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI聊天助手')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('''
            QMainWindow {
                background-color: #F5F5F5;
            }
            QTextEdit, QTextBrowser {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
            QComboBox, QCheckBox {
                font-family: Arial;
                font-size: 14px;
            }
        ''')
 
        # 创建窗口主部件和布局
        central_widget = QWidget()
        main_layout = QVBoxLayout()
 
        # 标题栏
        header_layout = QHBoxLayout()
        header_label = QLabel('你的个人AI助手')
        header_label.setFont(QFont('Arial', 16))
        header_layout.addWidget(header_label)
 
        # 功能区
        function_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['浅色', '深色'])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        function_layout.addWidget(QLabel('主题:'))
        function_layout.addWidget(self.theme_combo)
        function_layout.addSpacing(20)
 
        self.voice_check = QCheckBox('语音输入')
        function_layout.addWidget(self.voice_check)
        function_layout.addSpacing(20)
 
        self.emotion_check = QCheckBox('情感分析')
        self.emotion_check.setEnabled(False)  # Disable emotion analysis checkbox
        function_layout.addWidget(self.emotion_check)
        function_layout.addSpacing(20)
 
        self.tts_check = QCheckBox('语音输出')
        function_layout.addWidget(self.tts_check)
        function_layout.addStretch()
 
        # 模型选择区
        self.model_combo = QComboBox()
        self.update_model_list()  # 更新模型选择项
        function_layout.addWidget(QLabel('模型选择:'))
        function_layout.addWidget(self.model_combo)
        function_layout.addSpacing(20)
 
        # 添加模型按钮
        self.add_model_button = QPushButton('添加模型', clicked=self.add_model)
        function_layout.addWidget(self.add_model_button)
 
        # 添加帮助说明按钮
        self.help_button = QPushButton('帮助说明', clicked=self.show_help)
        function_layout.addWidget(self.help_button)
 
        # 消息历史区
        self.history_area = QTextBrowser()
        self.history_area.setReadOnly(True)
 
        # 输入区
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_box)
        self.send_button = QPushButton('发送', clicked=self.send_message)
        input_layout.addWidget(self.send_button)
 
        # 清空记录按钮
        self.clear_button = QPushButton('清空记录', clicked=self.clear_history)
        input_layout.addWidget(self.clear_button)
 
        # 导出记录按钮
        self.export_button = QPushButton('导出记录', clicked=self.export_history)
        input_layout.addWidget(self.export_button)
 
        # 添加部件到主布局
        main_layout.addLayout(header_layout)
        main_layout.addLayout(function_layout)
        main_layout.addWidget(self.history_area)
        main_layout.addLayout(input_layout)
 
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
 
        # 加载聊天记录
        self.load_history()
 
        # 初始化语音识别器
        self.recognizer = sr.Recognizer()
 
        # 初始化语音合成器
        self.engine = pyttsx3.init()
 
        # 绑定语音输入按钮点击事件
        self.voice_check.stateChanged.connect(self.toggle_voice_input)
 
        # 绑定语音输出按钮点击事件
        self.tts_check.stateChanged.connect(self.toggle_tts_output)
 
        # 模型列表
        self.models = ['模型A', '模型B']
 
    def add_model(self):
        dialog = AddModelDialog()
        dialog.exec_()
        # 添加模型后更新模型选择项
        self.update_model_list()
 
    def update_model_list(self):
        # 清空模型选择项
        self.model_combo.clear()
        # 扫描模型文件并将其名称添加到模型选择项中
        model_files = [file for file in os.listdir() if re.match(r"model_[a-zA-Z0-9]+\.py", file)]
        for model_file in model_files:
            model_name = os.path.splitext(model_file)[0]
            self.model_combo.addItem(model_name)
 
    def toggle_voice_input(self, state):
        if state == Qt.Checked:
            # 开始录音
            self.listen_thread = Thread(target=self.listen_to_audio)
            self.listen_thread.start()
        else:
            # 停止录音
            self.voice_check.setCheckState(Qt.Unchecked)
            self.listen_thread.join()
 
    def toggle_tts_output(self, state):
        if state == Qt.Checked:
            # 启用语音输出
            self.tts_enabled = True
        else:
            # 禁用语音输出
            self.tts_enabled = False
 
    def listen_to_audio(self):
        with sr.Microphone() as source:
            self.input_box.setPlaceholderText("请开始说话...")
            try:
                # 使用PocketSphinx引擎识别语音
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_sphinx(audio, language='zh-CN')
                self.input_box.setText(text)
            except sr.UnknownValueError:
                self.input_box.setPlaceholderText("无法识别，请重试...")
            except sr.RequestError:
                self.input_box.setPlaceholderText("无法连接到语音识别服务，请检查网络...")
 
    def send_message(self):
        user_input = self.input_box.text().strip()
        if user_input:
            # 获取当前时间戳
            timestamp = QDateTime.currentDateTime().toString('hh:mm')
            self.append_markdown_to_history(f'**[你] {timestamp}**\n{user_input}')
            self.input_box.clear()
 
            # 滚动到底部
            self.history_area.moveCursor(QTextCursor.End)
            self.history_area.ensureCursorVisible()  # 确保光标可见
 
            # 在新线程中生成回复
            Thread(target=self.generate_reply, args=(user_input, timestamp)).start()
 
    def generate_reply(self, user_input, timestamp):
        selected_model = self.model_combo.currentText()
        model_path = f"{selected_model}.py"
        spec = importlib.util.spec_from_file_location(selected_model, model_path)
        model_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_module)
        ai_reply = model_module.generate_response(user_input)
 
        # 在历史记录区域中添加 AI 回复
        self.append_markdown_to_history(f'**<span style="opacity:0.7">[AI助手] {timestamp}</span>**\n\n{ai_reply}')  # 添加一个换行符
        self.save_history(user_input, ai_reply, timestamp)
 
        # 滚动到底部
        self.history_area.moveCursor(QTextCursor.End)
        self.history_area.ensureCursorVisible()  # 确保光标可见
 
        # 如果启用语音输出，将 AI 回复转换为语音
        if hasattr(self, 'tts_enabled') and self.tts_enabled:
            self.speak(ai_reply)
 
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
 
    def change_theme(self, theme):
        if theme == '浅色':
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #F5F5F5;
                }
                QTextEdit, QTextBrowser {
                    background-color: #FFFFFF;
                    color: #333333;
                    border: 1px solid #CCCCCC;
                }
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #333333;
                    border: 1px solid #CCCCCC;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #0056B3;
                }
            ''')
        elif theme == '深色':
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #333333;
                }
                QTextEdit, QTextBrowser {
                    background-color: #444444;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                }
                QLineEdit {
                    background-color: #444444;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #0056B3;
                }
                QComboBox, QCheckBox {
                    color: #FFFFFF;
                }
            ''')
 
    def save_history(self, user_input, ai_reply, timestamp):
        data = {
            'user_input': user_input,
            'ai_reply': ai_reply,
            'timestamp': timestamp
        }
        with open('chat_history.json', 'a') as file:
            json.dump(data, file)
            file.write('\n')
 
    def load_history(self):
        try:
            with open('chat_history.json', 'r') as file:
                for line in file:
                    data = json.loads(line)
                    user_input = data['user_input']
                    ai_reply = data['ai_reply']
                    timestamp = data['timestamp']
                    self.append_markdown_to_history(f'**[你] {timestamp}**\n{user_input}')
                    self.append_markdown_to_history(f'**<span style="opacity:0.7">[AI助手] {timestamp}</span>**\n\n{ai_reply}')
        except FileNotFoundError:
            pass
 
    def append_markdown_to_history(self, markdown_text):
        html_text = markdown.markdown(markdown_text)
        self.history_area.append(html_text)
 
    def clear_history(self):
        # 清空聊天记录并重置界面
        self.history_area.clear()
        # 删除保存的历史记录文件
        try:
            os.remove('chat_history.json')
        except FileNotFoundError:
            pass
 
        # 弹出提示框
        QMessageBox.information(self, "提示", "聊天记录已清空！")
 
    def export_history(self):
        # 打开文件对话框以选择保存位置
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存聊天记录", "", "文本文件 (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    # 遍历历史记录区域中的文本并写入文件
                    text = self.history_area.toPlainText()
                    file.write(text)
                QMessageBox.information(self, "提示", "聊天记录已成功导出！")
            except Exception as e:
                QMessageBox.warning(self, "警告", f"导出聊天记录时出现错误：{str(e)}")
 
    def show_help(self):
        # 显示帮助说明对话框
        help_text = "这个程序是由aifeisheng开发的开源项目，代码已经在社区上公开。你可以自由添加所有AI模型，模型文件名称格式：model_[a-zA-Z0-9]+\.py ，例model_a.py、model_2.py。"
        QMessageBox.information(self, "帮助说明", help_text)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ChatWindow()
    main_window.show()
    sys.exit(app.exec_())