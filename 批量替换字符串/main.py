import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
 
class BatchReplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("批量替换工具")
        self.root.geometry("900x800")
        self.root.configure(bg='#F0F0F0')
 
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('TEntry', font=('Segoe UI', 10))
        self.style.configure('TLabel', font=('Segoe UI', 10), background='#F0F0F0')
        self.style.configure('TCheckbutton', font=('Segoe UI', 10), background='#F0F0F0')
 
        self.create_widgets()
 
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True)
 
        # Configure grid weights for responsiveness
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(1, weight=1)
 
        self.directory_label = ttk.Label(frame, text="目录:")
        self.directory_label.grid(row=0, column=0, sticky=tk.W, pady=(20, 5))
 
        self.directory_entry = ttk.Entry(frame, width=50)
        self.directory_entry.grid(row=0, column=1, pady=(20, 5), padx=(0, 10), sticky=tk.EW)
 
        self.select_directory_button = ttk.Button(frame, text="选择目录", command=self.select_directory)
        self.select_directory_button.grid(row=0, column=2, pady=(20, 5))
 
        self.old_str_label = ttk.Label(frame, text="旧字符串:")
        self.old_str_label.grid(row=1, column=0, sticky=tk.W, pady=5)
 
        self.old_str_entry = ttk.Entry(frame, width=50)
        self.old_str_entry.grid(row=1, column=1, pady=5, padx=(0, 10), sticky=tk.EW)
 
        self.new_str_label = ttk.Label(frame, text="新字符串:")
        self.new_str_label.grid(row=2, column=0, sticky=tk.W, pady=5)
 
        self.new_str_entry = ttk.Entry(frame, width=50)
        self.new_str_entry.grid(row=2, column=1, pady=5, padx=(0, 10), sticky=tk.EW)
 
        self.regex_label = ttk.Label(frame, text="使用正则表达式:")
        self.regex_label.grid(row=3, column=0, sticky=tk.W, pady=5)
 
        self.use_regex_var = tk.StringVar()
        self.use_regex_combobox = ttk.Combobox(frame, textvariable=self.use_regex_var, state="readonly", values=["是", "否"])
        self.use_regex_combobox.current(1)
        self.use_regex_combobox.grid(row=3, column=1, pady=5, padx=(0, 10), sticky=tk.W)
 
        self.create_backup_var = tk.BooleanVar(value=True)
        self.create_backup_checkbox = ttk.Checkbutton(frame, text="创建备份", variable=self.create_backup_var)
        self.create_backup_checkbox.grid(row=4, column=0, sticky=tk.W, pady=5)
 
        self.log_text = ScrolledText(frame, height=10, width=70, wrap=tk.WORD, font=('Segoe UI', 10))
        self.log_text.grid(row=5, column=0, columnspan=3, pady=5, padx=(0, 10), sticky=tk.NSEW)
 
        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=6, column=0, columnspan=3, pady=20, sticky=tk.EW)
 
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.grid(row=7, column=0, columnspan=3, pady=5)
 
        self.start_button = ttk.Button(frame, text="开始替换", command=self.start_replacing)
        self.start_button.grid(row=8, column=0, columnspan=3, pady=20)
 
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
 
    def start_replacing(self):
        directory = self.directory_entry.get()
        old_str = self.old_str_entry.get()
        new_str = self.new_str_entry.get()
        use_regex = self.use_regex_var.get() == "是"
        create_backup = self.create_backup_var.get()
 
        if not directory:
            messagebox.showwarning("错误", "请选择一个目录.")
            return
 
        if not old_str:
            messagebox.showwarning("错误", "请输入旧字符串.")
            return
 
        if not new_str:
            messagebox.showwarning("错误", "请输入新字符串.")
            return
 
        self.log_text.delete(1.0, tk.END)
        self.progress_bar["value"] = 0
 
        files_to_replace = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    files_to_replace.append(os.path.join(root, file))
 
        if not files_to_replace:
            messagebox.showinfo("信息", "没有找到任何.txt文件。")
            return
 
        self.progress_bar["maximum"] = len(files_to_replace)
 
        for index, file_path in enumerate(files_to_replace):
            self.replace_in_file(file_path, old_str, new_str, use_regex, create_backup)
            self.progress_bar["value"] = index + 1
            self.progress_label.config(text=f"进度: {index + 1}/{len(files_to_replace)}")
            self.root.update_idletasks()
 
        messagebox.showinfo("完成", "所有文件处理完毕!")
 
    def replace_in_file(self, file_path, old_str, new_str, use_regex, create_backup):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
 
            if use_regex:
                new_content = re.sub(old_str, new_str, content, flags=re.MULTILINE)
            else:
                new_content = content.replace(old_str, new_str)
 
            if create_backup:
                backup_file_path = file_path + '.bak'
                with open(backup_file_path, 'w', encoding='utf-8') as backup_file:
                    backup_file.write(content)
 
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
 
            self.log_text.insert(tk.END, f"成功替换: {file_path}\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"替换失败: {file_path} - {str(e)}\n")
 
if __name__ == "__main__":
    root = tk.Tk()
    app = BatchReplaceApp(root)
    root.mainloop()