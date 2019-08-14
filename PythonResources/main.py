"""
WM监测程序 - Created by sctop with Python
本程序将定期向WM服务器发送请求，并处理返回的数据为人类可读的语言。
本程序仅返回WM状态上标识为online(在线)或ingame(游戏中)的卖家信息。注意仅返回卖家信息。
本程序能识别物品是否为一个Mod，如果是则将所有卖家信息按Mod等级从高到低排序。
当有在线的卖家时，本程序将打印出卖家信息并默认播放指定路径下的提示音文件。

本程序仅在*Windows*平台下，使用Python 3.6.6版本测试过。其它系统与版本不保证能兼容。

本程序源代码所使用的外部库有：
pytz
playsound
这些库均可通过pip进行安装

本程序在发布时会附带Windows的可执行文件版本，请通过程序进入到主循环时的提示信息确认当前版本。
*Windows的可执行文件版本可能不会跟进源代码版本*

你可以在“Warframe中文维基”与“GitHub”上搜索“sctop”，相关程度最高的便是作者本人

Powered by Python with PyCharm
Edited by sctop
Version 1.0, 2019/08/10
"""

import sys
from data import get as get_data
from time import sleep
from new_time import format_time
from subprocess import call
from playsound import playsound
import json
from process_data import pricing, reputation

# 读取配置文件
try:
    with open("config.json", "r", encoding="UTF-8") as file:
        config = json.load(file)
except Exception:
    # 默认配置为开启提醒且每隔10分钟才查询一次
    default_config = {"sleep_time": 600, "alert": 1, "alert_filepath": "tips.mp3"}
    with open("config.json", "w", encoding="UTF-8") as file:
        json.dump(default_config, file, indent=4)
    config = default_config
# 提取配置内容
__SLEEPTIME__ = int(float(config["sleep_time"]))
__ALERTSTAT__ = int(float(config["alert"]))
__ALERTPATH__ = str(config["alert_filepath"])

# 获取物品名称
itemname = input("输入欲要监控的WM物品名称(英文)：")
# 小写全部字母，这是WM API的硬性要求
itemname = str(itemname).lower()
# 根据空格来分离逐个单词
temp = itemname.split(" ")
# 格式化物品名称（每个独立单词的中间都加上“_”）
itemname = ''
for i in range(len(temp)):
    itemname = itemname + temp[i]
    if i == len(temp) - 1:
        pass
    else:
        itemname = itemname + '_'

# 从服务器获取数据
req = get_data(itemname)
# 即便重试两次，服务器也亦不工作那么退出
if req == 1:
    input()
    sys.exit()

# 如果正常运行，那么刷新屏幕并作提示
call("cls", shell=True)
print(str(format_time("Asia/Taipei", None)) + ' WM监控程序 - V1.0 By sctop')
print(str(format_time("Asia/Taipei", None)) + ' 程序进入主循环。')
print(str(format_time("Asia/Taipei", None)) + ' 设定的欲监测物品名称：' + str(itemname) + '\n')

# 默认非Mod
itemtype = "normal"

# 主循环
while True:
    # 如果请求没有问题
    if req != 1:
        # 将req转换为json类型
        req = req.json()

        # 检测是一个Mod还是非Mod物品
        try:
            # 如果不是Mod，那么这一行代码将会引发错误进入到except代码段
            if req["payload"]["orders"][0]["mod_rank"] > -1:
                itemtype = "mod"
        except Exception:
            itemtype = "normal"

        # 读取数据并提取有用的数据
        info = []
        for i in req["payload"]["orders"]:
            # 只读取卖家
            if i["order_type"] == "sell":
                temp = {}
                temp["platform"] = i["platform"]
                temp["region"] = i["region"]
                temp["price"] = int(i["platinum"])
                temp["quantity"] = i["quantity"]
                temp["name"] = i["user"]["ingame_name"]
                temp["reputation"] = i["user"]["reputation"]
                temp["status"] = i["user"]["status"]
                # 如果是Mod，那么还需要加上Mod等级
                if itemtype == "mod":
                    temp["modrank"] = i["mod_rank"]
                info.append(temp)

        # 找到在线或游戏内玩家
        online = []
        for i in info:
            # 如果状态为online（在线）或ingame（游戏中）则加入online列表
            if i["status"] == "online" or i["status"] == "ingame":
                online.append(i)

        # 如果有玩家在线且为mod，则根据mod等级筛选
        if len(online) != 0 and itemtype == "mod":
            final = []
            current_rank = 15
            for i in range(current_rank + 1):
                for i in online:
                    if i["modrank"] == current_rank:
                        final.append(i)
                current_rank -= 1
            # 覆盖online为排序后的列表
            online = final

        online = reputation(itemtype, pricing(itemtype, online))

        # 本地化在线状态英文为中文
        for i in online:
            if i["status"] == "ingame":
                i["status"] = "游戏中"
            elif i["status"] == "online":
                i["status"] = "在线上"

        # 如果有任一卖家在线
        if len(online) != 0:
            print('\n' + str(format_time("Asia/Taipei", None)) + ' 程序监测到有在线的卖家：')
            output = ''
            num = 1
            # 一个接一个地输出信息
            for i in online:
                # 物品不是mod
                if itemtype == "normal":
                    output = output + "第{}号玩家：游戏内昵称：{}，客户端为{}；信誉度为{}，数量为{}，每一个售价{}白金；当前状态：{}".format(
                        str(num), i["name"], i["platform"], str(i["reputation"]), str(i["quantity"]), str(i["price"]),
                        i["status"]
                    ) + "\n"
                # 反之，则是一个mod
                elif itemtype == "mod":
                    output = output + "第{}号玩家：游戏内昵称：{}，客户端为{}；信誉度为{}，数量为{}；每一个Mod等级为{}，每一个售价{}白金；当前状态：{}".format(
                        str(num), i["name"], i["platform"], str(i["reputation"]), str(i["quantity"]), str(i["modrank"]),
                        str(i["price"]), i["status"]
                    ) + "\n"
                num += 1

            # 输出已经格式化好的内容
            print(output)

            # 如果提醒开启
            if __ALERTSTAT__ == 1:
                try:
                    playsound(__ALERTPATH__)
                except Exception as e:
                    print(str(format_time("Asia/Taipei", None)) + " 无法播放提示音。请在当前目录下复制一个名为“tips.mp3”的音频文件！")
                    print(str(format_time("Asia/Taipei", None)) + " 错误详细信息：" + str(e))

        else:
            print(str(format_time("Asia/Taipei", None)) + ' 当前程序未监测到有在线的卖家。')
    # 否则，这表明出了问题
    elif req == 1:
        print(str(format_time("Asia/Taipei", None)) + ' 程序暂时无法联系到服务器')

    # 睡眠一定时间，防止因请求过于频繁而触发IP封禁或服务器超载
    sleep(__SLEEPTIME__)
    # 重新从服务器获取数据
    req = get_data(itemname)
