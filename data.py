import requests
from new_time import format_time
from time import sleep
import json


# 获取API数据
def get_data(itemname):
    # 生成一个请求的链接
    json_url = "https://api.warframe.market/v1/items/{}/orders?include=item".format(itemname)
    # 保存由request返回的一个对象
    req = requests.get(json_url)
    # 404问题
    if req.status_code == 404:
        print(str(format_time("Asia/Taipei", None)) + " 检索失败，无法获取到该物品的信息。请确认是否输入正确！")
        return 1
    elif req.status_code == 403:
        print(str(format_time("Asia/Taipei", None)) + " 无权限在该服务器上检索，可能是因输入了部分特殊物品名或IP被封禁等。")
        return 1
    elif req.status_code != 200:
        print(str(format_time("Asia/Taipei", None)) + " 无法从服务器获取信息。")
        print(str(format_time("Asia/Taipei", None)) + " 错误代码：" + str(req.status_code))
        print(str(format_time("Asia/Taipei", None)) + " 5秒后重试。")
        sleep(5)
        req = requests.get(json_url)
        if req.status_code != 200:
            print(str(format_time("Asia/Taipei", None)) + " <<<!>>>网络连接无响应")
            print(str(format_time("Asia/Taipei", None)) + " 错误代码：" + str(req.status_code))
            return 1
        else:
            return req
    return req


# 配置
class Config:
    def get(self):
        try:
            with open("config.json", "r", encoding="UTF-8") as file:
                config = json.load(file)
        except Exception:
            # 默认配置为开启提醒且每隔10分钟才查询一次
            default_config = {"sleep_time": 600, "alert": 1, "alert_filepath": "tips.mp3", "last_item": "Unknown"}
            with open("config.json", "w", encoding="UTF-8") as file:
                json.dump(default_config, file, indent=4)
            config = default_config
        return config

    def config_update(self, itemname):
        with open("config.json", 'r', encoding='UTF-8') as file:
            temp = json.load(file)
        temp["last_item"] = itemname
        with open("config.json", 'w', encoding='UTF-8') as file:
            json.dump(temp, file)


# 获取物品名字
def get_name(mode, itemname):
    """
    用于在数据库中查找中英文

    :param mode: cTe -- chinese To english -- 中译英；
                 eTc -- english To chinese -- 英译中；
                 sTe -- search To english -- WM查找用英文 转换为 英文名称
                 eTs -- english To search -- 英文名称 转换为 WM查找用英文
    :param itemname: 字符串；欲查找的商品名称字符串
    :return: cTe/sTe返回英文，eTc返回中文，eTs返回*查询用*英文
    """
    with open("database.json", 'r', encoding='UTF-8') as file:
        temp = json.load(file)
    if mode == "cTe":
        for i in temp:
            if i["zh"] == itemname:
                return i["en"]
    elif mode == "eTc":
        for i in temp:
            if str(i["en"]).lower() == itemname.lower():
                return i["zh"]
    elif mode == "sTe":
        for i in temp:
            if i["search"] == itemname:
                return i["en"]
    elif mode == "eTs":
        for i in temp:
            if str(i["en"]).lower() == itemname.lower():
                return i["search"]
    return 1


# 获取用户输入
class GetInput:
    def tips(self):
        print("--------------------提示--------------------")
        print("本程序目前已经支持中文自动转成英文来自动查询")
        print("中英词库来自玩家云之幻 (Richasy)的个人贡献")
        print("感谢云之幻在GitHub上免费公开这些的全部内容")
        print("--------------特殊内容输入提示--------------")
        print("PRIME物品：[物品名]和 PRIME 之间要有空格")
        print("例如：“RHINO PRIME”或“犀牛 PRIME”")
        print("-----------------常用翻译-------------------")
        print("战甲：")
        print("set        → 一套")
        print("neuroptics → 头部神经光元")
        print("blueprint  → 蓝图")
        print("chassis    → 机体")
        print("systems    → 机体")
        print("虚空遗物类型：")
        print("lith → 古纪")
        print("meso → 前纪")
        print("neo  → 中纪")
        print("axi  → 后纪")
        print("虚空遗物优良率：")
        print("intact      → 完整")
        print("exceptional → 优良")
        print("flawless    → 无暇")
        print("radiant     → 光辉")
        print("其余内容请自行使用灰机wiki右侧工具栏快速查询翻译\n")

    def get_input(self):
        self.tips()
        # 获取内容
        itemname = input("输入欲要监控的WM物品名称(中英文皆可)：")
        en_name = get_name("cTe", itemname)
        if en_name != 1:
            en_name = get_name("eTs", en_name)
        else:
            en_name = get_name("eTs", itemname)
        itemname = en_name

        return itemname


# 获取标准化数据
class Standardize:
    def format_number(self, number, long=4):
        num_long = len(str(number))
        if num_long != long:
            need_add = long - num_long
            temp = list(str(number))
            for i in range(need_add):
                temp.insert(0, "0")
            temp2 = ""
            for i in temp:
                temp2 = temp2 + i
            temp2 = str(temp2)
            return temp2
        else:
            return number

    def adding_space(self, text, max_length):
        text_length = len(str(text))
        if text_length != max_length:
            temp = ""
            for i in range(max_length - text_length):
                temp = temp + " "
            return temp
        elif text_length >= max_length:
            return ""

    def max_length(self, object, sort_name):
        max_length = 0
        for i in object:
            if len(str(i[sort_name])) > max_length:
                max_length = len(str(i[sort_name]))
        return max_length
