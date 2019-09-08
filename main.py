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
Version 1.5, 2019/09/08
"""
# 外置模块
from data import get_data, get_name, Config, GetInput, Standardize
from new_time import format_time, sleep
from process_data import Sorting
import cursor
# 内置模块
from subprocess import call
from playsound import playsound
import requests, json, sys


def update_database():
    req = requests.get("https://raw.githubusercontent.com/Richasy/WFA_Lexicon/master/WF_Sale.json")
    if req.status_code != 200:
        print("更新失败")
        return 1
    req = req.json()
    with open("database.json", 'r', encoding='UTF-8') as file:
        content = json.load(file)
    if content != req:
        with open("database.json", 'w', encoding='UTF-8') as file:
            json.dump(req, file)
    print("更新成功")


print("正更新字典内容中......")
update_database()
call("cls", shell=True)
# 读取配置文件
config = Config().get()
# 提取配置内容
__SLEEPTIME__ = int(float(config["sleep_time"]))
__ALERTSTAT__ = int(float(config["alert"]))
__ALERTPATH__ = str(config["alert_filepath"])
__LASTITEM__ = str(config["last_item"])

# 记忆内容
if __LASTITEM__ != "Unknown":
    # 转换为中文
    LastitemCN = get_name("eTc", get_name("sTe", __LASTITEM__))
    if LastitemCN != 1:
        print("检测上一次您监控了 " + __LASTITEM__ + " (" + LastitemCN + ")")
    else:
        print("检测上一次您监控了 " + __LASTITEM__)
    print("您是否需要继续监控？[Y/N]", end='')
    temp = str(input())
    if temp.upper() == "Y":
        itemname = __LASTITEM__
    else:
        call("cls", shell=True)
        itemname = GetInput().get_input()
else:
    itemname = GetInput().get_input()

# 从服务器获取数据
req = get_data(itemname)
# 即便重试两次，服务器也亦不工作那么退出
if req == 1:
    input()
    sys.exit()

# 正常运行，写入文件
Config().config_update(itemname)

# 默认非Mod
itemtype = "normal"

# 主循环
while True:
    # 如果正常运行，那么刷新屏幕并作提示
    call("cls", shell=True)
    print(str(format_time("Asia/Taipei", None)) + ' WM监控程序 - V1.5 By sctop')
    print(str(format_time("Asia/Taipei", None)) + ' 程序进入主循环。')
    en_name = get_name("sTe", itemname)
    cn_name = get_name("eTc", en_name)
    print(str(format_time("Asia/Taipei", None)) + ' 设定的欲监测物品名称：' + en_name + '(' + cn_name + ')')
    print(str(format_time("Asia/Taipei", None)) + ' 当前程序每隔' + str(__SLEEPTIME__) + '秒查询一次\n')
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

        # 筛选
        online = Sorting().reputation(itemtype, Sorting().pricing(itemtype, online))

        # 如果有任一卖家在线
        if len(online) != 0:
            print('\n' + str(format_time("Asia/Taipei", None)) + ' 程序监测到有在线的卖家：')
            output = ''
            num = 1
            Standard = Standardize()

            # 最大值，用于优化UI
            max_number_length = len(str(len(online)))
            max_name_length = Standard.max_length(online, "name")
            max_reputation_length = Standard.max_length(online, "reputation")
            max_quantity_length = Standard.max_length(online, "quantity")
            max_price_length = Standard.max_length(online, "price")
            if itemtype == "mod":
                max_rank_length = Standard.max_length(online, "modrank")

            # 一个接一个地输出信息
            for i in online:
                # 物品不是mod
                if itemtype == "normal":
                    print("第{}号玩家: 游戏内昵称:{},客户端为{};信誉度为{},数量为{},每一个售价{}白金  当前状态:{}".format(
                        str(Standard.format_number(num, max_number_length)),
                        i["name"] + Standard.adding_space(i["name"], max_name_length),
                        i["platform"],
                        str(i["reputation"]) + Standard.adding_space(str(i["reputation"]), max_reputation_length),
                        str(i["quantity"]) + Standard.adding_space(str(i["quantity"]), max_quantity_length),
                        str(i["price"]) + Standard.adding_space(str(i["price"]), max_price_length),
                        i["status"]), end=''
                    )
                # 反之，则是一个mod
                elif itemtype == "mod":
                    print("第{}号玩家: 游戏内昵称:{},客户端为{};信誉度为{},数量为{};每一个Mod等级为{},每一个售价{}白金  当前状态：{}".format(
                        str(Standard.format_number(num, max_number_length)),
                        i["name"] + Standard.adding_space(i["name"], max_name_length),
                        i["platform"],
                        str(i["reputation"]) + Standard.adding_space(str(i["reputation"]), max_reputation_length),
                        str(i["quantity"]) + Standard.adding_space(str(i["quantity"]), max_quantity_length),
                        str(i["modrank"]) + Standard.adding_space(str(i["modrank"]), max_rank_length),
                        str(i["price"]) + Standard.adding_space(str(i["price"]), max_price_length),
                        i["status"]), end=''
                    )
                sys.stdout.flush()
                print("\n", end='')
                sys.stdout.flush()
                num += 1

            # 输出已经格式化好的内容
            print(output)

            # 移动光标至第一行开始位置，这样就可以强制窗口滚动
            cursor.move(0, 0)

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
