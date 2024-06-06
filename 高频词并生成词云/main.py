import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
 
# 读取要分析的txt文档，注意修改为自己的文件名[/size]
[size=3]with open('concatenated.txt', 'r', encoding='utf-8') as f:
    s = f.read()
# 使用jieba进行分词
jieba.load_userdict('cidian.txt')#可以注释掉以使用默认词典
text = jieba.cut(s)
stopwords = {}.fromkeys([ line.rstrip() for line in open('cn_stopwords.txt',encoding='utf-8') ])  #记得改为自己的停用词文件名
words = [word for word in text if word not in stopwords]  # 去除停顿词
 
# 统计词频
word_count = Counter()
for word in words:
    if len(word) >= 2:  # 仅统计长度大于等于2的词语
        word_count[word] += 1
# 获取词频前100的词汇
top100_words = word_count.most_common(100)
# 输出结果到txt文档
with open('top100词频.txt', 'w', encoding='utf-8-sig') as f:
    for word, count in top100_words:
        f.write(f'{word}: {count}\n')
         
text2 = ' '.join(words)#用空格连接分词
 
mask = np.array(Image.open("mask_pic.jpg")) #将图片转换为数组。记得修改为自己图片的文件名
 
ciyun = WordCloud(font_path="字体.ttf",   #字体选用自己电脑上的汉语字体，删掉可能会乱码
               mask=mask, #注释掉这一行，生成默认矩形图
               width = 1000,  #长
               height = 700,  #宽
               background_color='white',  #背景颜色
               max_words=100,#最多词数
               max_font_size=100,#字号最大值
               ).generate(text2)
 
 
# 显示词云，这一块可以直接删掉，不影响生成词云，只不过不会在IDE中显示
plt.imshow(ciyun, interpolation='bilinear')# 用plt显示图片
plt.axis("off")  # 不显示坐标轴
plt.show() # 显示图片
 
# 保存到文件
ciyun.to_file("词云.png")