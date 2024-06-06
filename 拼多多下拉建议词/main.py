##### 拼多多下拉建议词批量获取[/size][/font][font=微软雅黑][size=3]# BY:lx
import requests
import json
import datetime
import csv
from prettytable import PrettyTable
# 创建表头
header = ['序号','关键词' ]
# 创建表格格式方法
x = PrettyTable()
x.field_names = header  # 设置表格标题名称
now = datetime.datetime.now()
times= now.strftime("%Y-%m-%d %H-%M-%S")
def get_suggestions(keyword):
    session = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
 
    url = f"https://mobile.yangkeduo.com/proxy/api/search_suggest?&query={keyword}"
    try:
        start_time = datetime.datetime.now()
        response = session.get(url, headers=headers)
        data = json.loads(response.text)
        suggestions = []
        for suggest in data["suggest"]:
            kw_suggest = suggest
            url2 = f'https://mobile.yangkeduo.com/proxy/api/search_suggest?&query={kw_suggest}'
            try:
                response_suggest = session.get(url2, headers=headers)
                list(set(response_suggest)) ##去重处理
                data_suggest = json.loads(response_suggest.text)
                suggestions.extend(data_suggest["suggest"])
            except Exception as e:
                print(f"获取建议词失败：{e}")
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time
        return suggestions, time_taken.total_seconds()
    except Exception as e:
        print(f"获取建议词失败：{e}")
        return [], 0
 
#保存表格
def export_to_csv(filename, suggestions):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['序 号','关键词'])
        num = 0
        for suggestion in suggestions:
            num +=1
            writer.writerow([num,suggestion])
 
def main():
    keyword = input("\n请输入你要查询的关键词‘按回车键’搜索：")
    print(f"正在获取拼多多搜索下拉'{keyword}'的建议词，请稍等.......")
    suggestions, time_taken = get_suggestions(keyword)
    con = 0
    for suggestion in suggestions:
        con += 1
        x.add_row([con,suggestion])
 # 导出到CSV文件
    kw_filename = f"{keyword}下拉建议词.csv"
    export_to_csv(kw_filename, suggestions)
    print(x) #打印获取到的数据
# 输出信息
    print(f"=================================================\n"
          f"总共获取到'{keyword}' {len(suggestions)} 条关键词数据\n"
          f"本次获取耗时：{time_taken} 秒\n"
          f"当前获取时间为：{times} \n"
          f" BY：LX 本程序仅供交流学习！\n"
          f"文件已成功导出在同软件目录下，请处理查看！文件名为：{kw_filename}\n"
          f"===================================================")
    input("请按任意键退出程序！")
if __name__ == '__main__':
    main()