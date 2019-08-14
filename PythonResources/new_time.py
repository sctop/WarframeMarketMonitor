import pytz, datetime


def format_time(tz, mode):
    """
    此函数用于格式化一个基于现在时间的时间字符串

    :param tz: 传入一个时区。对于中国地区请使用“Asia/Taipei”，可使用简写
    :param space: 是否需要空格，一般情况下作文件名。
    :return: 非不需要空格情况下，函数将返回格式为“YY-MM-DD HH-MM-SS 时区”
    """
    # 本地时间时区设定
    tz_set = pytz.timezone(tz)
    # 年月日，格式“YY-MM-DD”
    if mode == "nospace":
        yymmdd = datetime.datetime.now(tz_set).strftime("%Y-%m-%d")
    else:
        yymmdd = datetime.datetime.now(tz_set).strftime("%Y-%m-%d ")
    # 时分秒
    if mode == "nospace":
        hhmmss = datetime.datetime.now(tz_set).strftime("%H%M%S")
    else:
        hhmmss = datetime.datetime.now(tz_set).strftime("%H:%M:%S")
    if mode == "log":
        timezone = datetime.datetime.now(tz_set).strftime(" %z")
    else:
        timezone = ""
    return yymmdd + hhmmss + timezone
