方法一： 使用time.sleep()基础函数实现简单定时任务
import time
 
def simple_task():
    print("任务执行时间：", time.ctime())
 
# 每隔5分钟执行一次任务
while True:
    simple_task()
    time.sleep(5 * 60)
 
方法二： 结合系统定时任务（如cron）执行Python脚本
Linux (cron):
在用户家目录下编辑crontab文件：
crontab -e
添加定时任务条目：
0 3 * * * /usr/bin/python3 /path/to/your/script.py
上述cron表达式表示每天凌晨3点执行指定Python脚本。