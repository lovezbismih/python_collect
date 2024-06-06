import tkinter as tk
from tkinter import filedialog
import requests
import urllib3
import pyperclip
import base64
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
 
def upload_image():
    url = "aHR0cHM6Ly9iYWlqaWFoYW8uYmFpZHUuY29tL3BjdWkvcGljdHVyZS91cGxvYWQ="
    url = base64.b64decode(url).decode("utf-8")
    print(url)
    custom_cookie = cookie_entry.get(
        "1.0", tk.END
    ).strip() 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30",
        "Cookie": custom_cookie,
    }
    file_path = filedialog.askopenfilename()
    files = {"media": open(file_path, "rb")}
    response = requests.post(url, headers=headers, files=files)
 
    if response.status_code == 200:
        data = response.json()
        url = data["ret"]["https_url"]
        result_label.config(text="上传成功，图片链接为：" + url)
         
        copy_button.config(state=tk.NORMAL)  
        global success_url
        success_url = url  
    else:
        result_label.config(text="上传失败，错误信息为：" + response.text)
 
 
def copy_url_to_clipboard():
    pyperclip.copy(success_url)  
    result_label.config(text="已复制到剪贴板")
 
 
# 创建GUI窗口
root = tk.Tk()
root.title("百家号变图床 - By wkdxz")
 
root.geometry("370x150") 
 
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry("+{}+{}".format(position_right, position_down))
 
cookie_label = tk.Label(
    root, text="输入Cookie（登录百家号，然后按F12拿Cookie，不会就搜索）"
)
cookie_label.pack()
 
cookie_entry = tk.Text(root, height=4, width=50)
cookie_entry.pack()
 
button_frame = tk.Frame(root)
button_frame.pack()
 
upload_button = tk.Button(button_frame, text="上传图片", command=upload_image)
upload_button.pack(side=tk.LEFT, padx=10, pady=5)
 
copy_button = tk.Button(
    button_frame, text="复制URL", command=copy_url_to_clipboard, state=tk.DISABLED
)  # 初始状态为禁用
copy_button.pack(side=tk.LEFT, padx=10, pady=5)
 
result_label = tk.Label(root, text="")
result_label.pack()
 
root.mainloop()