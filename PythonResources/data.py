import requests
from new_time import format_time
from time import sleep
import json

def get(itemname):
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


def cTe(itemname):
    with open("database.json", 'r', encoding='UTF-8') as file:
        temp = json.load(file)

    for i in temp:
        if i["zh"] == itemname:
            return i["search"]

    return 1


def config():
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


def config_update(itemname):
    with open("config.json", 'r', encoding='UTF-8') as file:
        temp = json.load(file)
    temp["last_search"] = itemname
    with open("config.json", 'w', encoding='UTF-8') as file:
        json.dump(temp, file)
