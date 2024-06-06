import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import random

def generate_sign(timestamp, secret):
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign

def clear_cache(image_path):
    try:
        os.remove(image_path)
        print(f"缓存文件已删除: {image_path}")
    except FileNotFoundError:
        print(f"缓存文件不存在: {image_path}")

def download_image(url, folder_path, filename):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_path = os.path.join(folder_path, filename)

    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"图片下载成功: {image_path}")
        return image_path
    else:
        print(f"图片下载失败: {url}")
        return None

def upload_image_to_server(local_image_path):
    # 模拟上传图片到服务器，并生成一个带有唯一参数的URL
    # 这里的实现根据实际的上传服务可能有所不同
    server_url = 'https://www.abc.com/60s/01.jpg'
    unique_param = random.randint(1000, 9999)  # 生成随机参数避免缓存
    full_url = f"{server_url}?v={unique_param}"
    print(f"图片已上传到服务器: {full_url}")
    return full_url

def send_image_to_dingtalk(image_url, robot_webhook, secret):
    timestamp = str(round(time.time() * 1000))
    sign = generate_sign(timestamp, secret)
    webhook_url = f"{robot_webhook}&timestamp={timestamp}&sign={sign}"

    # 构建消息内容
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "60s图片的自定义内容",
            "text": f"![image]({image_url})"
        }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200 and response.json().get('errcode') == 0:
        print("图片发送成功")
    else:
        print("图片发送失败")
        print(response.text)

# 主函数
def main():
    folder_path = '60s'
    filename = '01.jpg'
    image_path = os.path.join(folder_path, filename)
    
    # 清除缓存文件
    clear_cache(image_path)
    
    image_source_url = 'https://api.03c3.cn/api/zb'
    
    # 先下载图片并保存
    local_image_path = download_image(image_source_url, folder_path, filename)
    
    if local_image_path:
        # 上传图片到服务器并获取新URL
        local_server_image_url = upload_image_to_server(local_image_path)
        
        robot_webhook = 'https://oapi.dingtalk.com/robot/send?access_token=###'
        secret = '###'
        
        # webhook里是机器人地址，secret是加签
        send_image_to_dingtalk(local_server_image_url, robot_webhook, secret)

if __name__ == '__main__':
    main()
