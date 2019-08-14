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
from data import get as get_data, cTe, config, config_update
from time import sleep
from new_time import format_time
from subprocess import call
from playsound import playsound
from process_data import pricing, reputation
import sys


def tips():
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

# 读取配置文件
config = config()
# 提取配置内容
__SLEEPTIME__ = int(float(config["sleep_time"]))
__ALERTSTAT__ = int(float(config["alert"]))
__ALERTPATH__ = str(config["alert_filepath"])
__LASTITEM__ = str(config["last_item"])

# 记忆内容
if __LASTITEM__ != "Unknown":
    print("检测上一次您监控了 " + __LASTITEM__)
    print("您是否需要继续监控？[Y/N]", end='')
    temp = input()
    if temp == "Y":
        itemname = __LASTITEM__
else:
    tips()
    # 获取内容
    itemname = input("输入欲要监控的WM物品名称(中英文皆可)：")
    en_name = cTe(itemname)
    if en_name != 1:
        itemname = en_name
    else:
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

# 正常运行，写入文件
config_update(itemname)
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

        # 如果有任一卖家在线
        if len(online) != 0:
            print('\n' + str(format_time("Asia/Taipei", None)) + ' 程序监测到有在线的卖家：')
            output = ''
            num = 1
            # 一个接一个地输出信息
            for i in online:
                # 物品不是mod
                if itemtype == "normal":
                    print("第{}号玩家：游戏内昵称：{}，客户端为{}；信誉度为{}，数量为{}，每一个售价{}白金；当前状态：{}".format(
                        str(num), i["name"], i["platform"], str(i["reputation"]), str(i["quantity"]), str(i["price"]),
                        i["status"]), end=''
                    )
                # 反之，则是一个mod
                elif itemtype == "mod":
                    print("第{}号玩家：游戏内昵称：{}，客户端为{}；信誉度为{}，数量为{}；每一个Mod等级为{}，每一个售价{}白金；当前状态：{}".format(
                        str(num), i["name"], i["platform"], str(i["reputation"]), str(i["quantity"]), str(i["modrank"]),
                        str(i["price"]), i["status"]), end=''
                    )
                sys.stdout.flush()
                print("\n", end='')
                sys.stdout.flush()
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
