import urllib.parse
 
while True:  # 创建一个循环，让用户可以多次输入直到选择退出
    # 提示用户输入语句
    s = input("请输入将要转换为IBM037编码的语句（输入'exit'以退出）: ")
 
    # 检查用户是否想要退出
    if s.lower() == 'exit':
        print("程序已退出。")
        break  # 使用break跳出循环，结束程序
 
    try:
        # 尝试将输入的字符串转换为IBM037编码并进行URL编码
        ens = urllib.parse.quote(s.encode('ibm037'))
        # 显示转换后的结果
        print("转换后的结果为:", ens)
    except LookupError:
        # 如果编码不支持，捕获异常并给出提示
        print("编码错误：IBM037编码可能不受支持或输入包含无法编码的字符。")