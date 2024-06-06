import requests
from lxml import etree
 
CODE_ST = 58344  # 十六进制e3e8的十进制
CODE_ED = 58715  # 十六进制e55b的十进制
charset = ['D', '在', '主', '特', '家', '军', '然', '表', '场', '4', '要', '只', 'v', '和', '?', '6', '别', '还', 'g',
           '现', '儿', '岁', '?', '?', '此', '象', '月', '3', '出', '战', '工', '相', 'o', '男', '首', '失', '世', 'F',
           '都', '平', '文', '什', 'V', 'O', '将', '真', 'T', '那', '当', '?', '会', '立', '些', 'u', '是', '十', '张',
           '学', '气', '大', '爱', '两', '命', '全', '后', '东', '性', '通', '被', '1', '它', '乐', '接', '而', '感',
           '车', '山', '公', '了', '常', '以', '何', '可', '话', '先', 'p', 'i', '叫', '轻', 'M', '士', 'w', '着', '变',
           '尔', '快', 'l', '个', '说', '少', '色', '里', '安', '花', '远', '7', '难', '师', '放', 't', '报', '认',
           '面', '道', 'S', '?', '克', '地', '度', 'I', '好', '机', 'U', '民', '写', '把', '万', '同', '水', '新', '没',
           '书', '电', '吃', '像', '斯', '5', '为', 'y', '白', '几', '日', '教', '看', '但', '第', '加', '候', '作',
           '上', '拉', '住', '有', '法', 'r', '事', '应', '位', '利', '你', '声', '身', '国', '问', '马', '女', '他',
           'Y', '比', '父', 'x', 'A', 'H', 'N', 's', 'X', '边', '美', '对', '所', '金', '活', '回', '意', '到', 'z',
           '从', 'j', '知', '又', '内', '因', '点', 'Q', '三', '定', '8', 'R', 'b', '正', '或', '夫', '向', '德', '听',
           '更', '?', '得', '告', '并', '本', 'q', '过', '记', 'L', '让', '打', 'f', '人', '就', '者', '去', '原', '满',
           '体', '做', '经', 'K', '走', '如', '孩', 'c', 'G', '给', '使', '物', '?', '最', '笑', '部', '?', '员', '等',
           '受', 'k', '行', '一', '条', '果', '动', '光', '门', '头', '见', '往', '自', '解', '成', '处', '天', '能',
           '于', '名', '其', '发', '总', '母', '的', '死', '手', '入', '路', '进', '心', '来', 'h', '时', '力', '多',
           '开', '己', '许', 'd', '至', '由', '很', '界', 'n', '小', '与', 'Z', '想', '代', '么', '分', '生', '口',
           '再', '妈', '望', '次', '西', '风', '种', '带', 'J', '?', '实', '情', '才', '这', '?', 'E', '我', '神', '格',
           '长', '觉', '间', '年', '眼', '无', '不', '亲', '关', '结', '0', '友', '信', '下', '却', '重', '己', '老',
           '2', '音', '字', 'm', '呢', '明', '之', '前', '高', 'P', 'B', '目', '太', 'e', '9', '起', '稜', '她', '也',
           'W', '用', '方', '子', '英', '每', '理', '便', '西', '数', '期', '中', 'C', '外', '样', 'a', '海', '们',
           '任']
 
 
# 解析章节加密内容
def interpreter(cc):  # 原字符减去e338获取到另一套字体的该编码字符
    bias = cc - CODE_ST
    if charset[bias] == '?':  # 特殊处理
        return chr(cc)
    return charset[bias]
 
 
cap_url = 'https://fanqienovel.com/api/reader/full?itemId=6893843740742386183'
cap02_url = 'https://fanqienovel.com/reader/6893843740910158344'
# cap02_url = 'https://fanqienovel.com/reader/6893843740834660878?enter_from=reader'
# cap03_url = 'https://fanqienovel.com/reader/6893843740910158344?enter_from=reader'
 
fp = open('人类不死以后.txt', 'a', encoding='utf-8')
 
headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
 
"""第一章爬取"""
content_url = 'http://fanqienovel.com/reader/6893843740742386183'
response = requests.get(url=content_url, headers=headers)
tree = etree.HTML(response.text)
 
title = tree.xpath('//h1[[url=home.php?mod=space&uid=341152]@Class[/url] = "muye-reader-title"]/text()')
fp.write(title[0] + '\n')
 
content_tags = tree.xpath('//div[@class="muye-reader-content noselect"]/div//p/text()')
# 获取小说章节
# print(title)
content = []
for content_tag in content_tags:
    para = ''
    for char in content_tag:
        cc = ord(char)
        if CODE_ST <= cc <= CODE_ED:
            ch = interpreter(cc)
            para += ch
        else:
            para += char  # 这里应该是拼接字符，而不是其ASCII码
    content.append(para)
 
# print(content)
print('正在下载第1章')
for para in content:
    fp.write('    ')
    fp.write(para)
    fp.write('\n')
 
index = 1
while True:
    # TODO:获取下一章节ID
    response = requests.get(url=cap_url, headers=headers)
 
    data = response.json()
 
    json_obj = response.json()  # 解析JSON数据为Python字典
 
    next_id = json_obj['data']['chapterData']['nextItemId']  # 解嵌套
 
    next_id_url = 'https://fanqienovel.com/api/reader/full?itemId=' + str(next_id)
 
    next_content_url = 'http://fanqienovel.com/reader/' + str(next_id)
 
    # print(next_id_url)
 
    cap_url = next_id_url  # 迭代更新获取下一章id的url
 
    # TODO:获取每章节内容
    response = requests.get(url=next_content_url, headers=headers)
 
    tree = etree.HTML(response.text)
 
    title = tree.xpath('//h1[@class = "muye-reader-title"]/text()')
    fp.write(title[0] + '\n')
 
    content_tags = tree.xpath('//div[@class="muye-reader-content noselect"]/div//p/text()')
 
    # print(len(content_tags))
 
    # 获取小说章节
    content = []
    for content_tag in content_tags:
        para = ''
        for char in content_tag:
            cc = ord(char)
            if CODE_ST <= cc <= CODE_ED:
                ch = interpreter(cc)
                para += ch
            else:
                para += char  # 这里应该是拼接字符，而不是其ASCII码
        content.append(para)
 
    # print(content)
    index += 1
 
    for para in content:
        fp.write('    ')
        fp.write(para)
        fp.write('\n')
    print('正在下载第' + str(index) + '章')