import re

# 假设输入的字符串如下
input_string = "masterpiece,sexy,1girl,2boys,hot"

# 正则
pattern = r"\D*girls|\D*boys"


# 定义一个函数来处理输入字符串
def extract_tags(input_str):
    # 将输入字符串分割成列表
    str_list = input_str.split(",")

    # 初始化变量来存储结果
    characternumber = []
    others = []

    # 遍历列表
    for item in str_list:
        if item in ["1girl", "1boy"]:
            characternumber.append(item)
        if re.search(pattern, item):
            characternumber.append(item)
        others.append(item)

    # 返回处理后的结果
    return characternumber, others
