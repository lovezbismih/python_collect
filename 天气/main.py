import requests
import time
import hmac
import hashlib
import base64

def get_weather(city):
    api_key = '###'  # 替换为您的心知天气 API 密钥
    url = f'https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={city}&language=zh-Hans'
    response = requests.get(url)
    print(f"Requesting weather data with URL: {url}")

    if response.status_code != 200:
        print(f"Failed to get weather data: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    if 'results' in data and data['results']:
        weather_info = data['results'][0]['now']
        weather_desc = weather_info['text']
        weather_icon = get_weather_icon(weather_desc)
        temperature = weather_info['temperature']
        return weather_desc, weather_icon, temperature
    else:
        print("No results found in weather data")
        return None

def get_weather_forecast(city):
    api_key = '###'  # 替换为您的心知天气 API 密钥
    url = f'https://api.seniverse.com/v3/weather/daily.json?key={api_key}&location={city}&language=zh-Hans&days=3'
    response = requests.get(url)
    print(f"Requesting weather forecast data with URL: {url}")

    if response.status_code != 200:
        print(f"Failed to get weather forecast data: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    if 'results' in data and data['results']:
        forecasts = data['results'][0]['daily']
        return forecasts
    else:
        print("No results found in weather forecast data")
        return None

def get_weather_icon(weather_desc):
    if '晴' in weather_desc:
        return '☀️'
    elif '多云' in weather_desc:
        return '☁️'
    elif '雨' in weather_desc:
        return '🌧️'
    else:
        return ''

def send_to_dingtalk(message, webhook_url, secret):
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    sign = base64.b64encode(hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()).decode()
    final_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"
    headers = {'Content-Type': 'application/json'}
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': '天气提醒',
            'text': message
        }
    }
    response = requests.post(final_url, json=data, headers=headers)
    if response.status_code == 200:
        print("Message sent successfully to DingTalk!")
    else:
        print(f"Failed to send message to DingTalk: {response.status_code}")

def read_city_from_file(file_path):
    with open(file_path, 'r') as file:
        city = file.readline().strip()
    return city

# 从环境变量中获取钉钉机器人的 Webhook URL 和密钥
webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=####'  # 替换为您的钉钉机器人的 Webhook URL
secret = '###'  # 替换为您的钉钉机器人的密钥

# 从文件中读取城市名称
#city_file_path = 'city.txt'  # 城市名称文件路径
#city = read_city_from_file(city_file_path)
city =  "西安"
print(f"读取的城市名称: {city}")

# 获取天气信息
weather_data = get_weather(city)
forecasts = get_weather_forecast(city)

# 构建消息内容
if weather_data and forecasts:
    weather_desc, weather_icon, temperature = weather_data
    message = f"### 今日天气提醒\n\n城市：{city}\n天气：{weather_icon} {weather_desc}\n温度：{temperature}°C\n\n【未来3天天气预报】\n\n"
    for forecast in forecasts:
        date = forecast['date']
        weather_desc = forecast['text_day']
        temperature_high = forecast['high']
        temperature_low = forecast['low']
        message += f"{date}: {weather_desc}, 温度：{temperature_low}°C ~ {temperature_high}°C\n\n"
else:
    message = "未能获取到天气信息，请检查城市名称。"

# 发送消息到钉钉机器人
send_to_dingtalk(message, webhook_url, secret)
