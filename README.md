# WarframeMarketMonitor
这是一个小巧的，基于Python与命令行窗口的Warframe Market物品监控程序。

您可以通过发起一个PR来请求源码更新。或者如果您遇到了问题，请提交一个issue。

## 感谢
感谢GitHub用户[Richasy(云之幻)](https://github.com/Richasy)提供的[中英对照数据](https://github.com/Richasy/WFA_Lexicon)，如果没有这份数据的存在本程序的中英转换功能就不复存在。大家可以去项目页面star或者follow一下他本人呢！

## 下载
如果您的电脑上安装了Python 3或更高版本，则请在[此处下载](PythonResources.zip)

如果您是普通用户，或不确定是否拥有Python，请在[此处下载](WindowsVersion.zip)

## 程序工作原理
本程序定期向WarframeMarket的API域名发出请求，并将请求的内容处理最后输出为人类可读与理解的内容到命令行窗口内。如果有卖家，则发出提示音提示用户。

其中，间隔时间将由目录下的“config.json”的键“sleep_time”的值所确定（单位：秒）。

## 程序默认值
第一次使用程序时，程序将自动创建包含以下内容的JSON文件：
```json
{
    "sleep_time": 600,
    "alert": 1,
    "alert_filepath": "tips.mp3",
    "last_item": "Unknown"
}
```
在其中，

1. “sleep_time”定义前一次与下一次请求之间的间隔（时间差），单位为秒，默认600秒（10分钟）
2. “alert”定义是否需要提示音的提示，值为“0”或“1”，默认为“1”（开启），反之亦然
3. “alert_filepath”定义提示音文件的路径，默认为“tips.mp3”。注意其**仅支持mp3格式**的音频文件
4. “last_item”定义上一次有效的查询的物品名称

您可以通过修改配置文件的内容来达到您想要的效果。

## 程序特性
- [x] 使用方法简单快捷
- [x] 支持英文物品名搜索
- [x] 支持当有卖家时发出提示音提醒
- [x] 支持对Mod等级进行排序
- [x] 支持对同等级Mod的价格排序
- [x] 支持对同价格Mod的信誉排序
- [x] 支持中文物品名转换为英文来进行搜索
- [x] 支持下一次打开程序时提示是否要继续监控上次关闭时的物品
- [x] 支持自动更新字典
- [x] 支持每次输出结果后都刷新屏幕，减少冗余信息
- [x] 支持输出完后屏幕自动回到首行，便于直接查看
- [x] 优化User Interface

## 二次开发
本程序使用了以下外部库。这些库分别是：

- pytz
- playsound

这些库均可以通过pip进行安装。懒人代码如下：

```
pip install pytz
pip install playsound
```

对于Windows用户，如果上面的代码不奏效，请使用以下代码：

```
py -m pip install pytz
py -m pip install playsound
```

## 版本记录
```
V1.4 @ 2019-09-07
源代码增加新功能，修复Bug
Windows Exe可执行文件更新至V1.4

V1.3 @ 2019-08-14
源代码增加新功能，此时已经基本完善
Windows Exe可执行文件更新至V1.3

V1.2 @ 2019-08-14
源代码添加新功能
Windows Exe可执行文件更新至V1.2

V1.1 @ 2019-08-14
源代码增加新功能
Windows Exe可执行文件维持V1.0状态

V1.0 @ 2019-08-10
程序制作完成，发布到GitHub上
```