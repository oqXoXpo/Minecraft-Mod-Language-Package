#!/usr/bin/python3
import pymysql
import os


# 获取语言文件，处理得到一个 dict
def lang_to_dict(file_path):
    lang_dict = {}
    with open(file_path, 'r', errors='ignore') as f:
        for line in f.readlines():
            if line != None and line[0] != '#' and line[0] != '/' and '=' in line:
                # 剔除行末尾 \n
                line = line.rstrip('\n')
                line_list = line.split('=', 1)
                lang_dict[line_list[0]] = line_list[1]
    return lang_dict


# 打开数据库连接
db = pymysql.connect(host='localhost', user='',
                     passwd='', db='test', charset='utf8mb4')
# 创建一个游标对象 cursor
cursor = db.cursor()
# 如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS LANG")

# 使用预处理语句创建表
# 限定只装入 16 字符汉字，256 字符英文
cursor.execute("""CREATE TABLE LANG (
         modid varchar(64),
         en_us varchar(256),
         zh_cn varchar(16))
         CHARSET=utf8mb4""")

# 开始遍历文件了
for modid in os.listdir('project/assets'):
    # 先判定 en_us.lang 是否存在
    if not os.path.exists('project/assets/{}/lang/en_us.lang'.format(modid)):
        continue
    # 而后开始转换为 dict
    en_us_dict = lang_to_dict(
        'project/assets/{}/lang/en_us.lang'.format(modid))
    zh_cn_dict = lang_to_dict(
        'project/assets/{}/lang/zh_cn.lang'.format(modid))

    # 开始写入数据库
    for k in zh_cn_dict.keys():
        if k in en_us_dict:
            if len(en_us_dict[k]) <= 256 and len(zh_cn_dict[k]) <= 16 and '"' not in en_us_dict[k] and '"' not in zh_cn_dict[k]:
                sql = '''INSERT INTO LANG (modid, en_us, zh_cn)
                         VALUES ("{}", "{}", "{}")'''.format(modid, en_us_dict[k], zh_cn_dict[k])
                cursor.execute(sql)

db.commit()
# 关闭数据库连接
db.close()
