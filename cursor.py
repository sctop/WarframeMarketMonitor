"""
以前研究光标移动的时候发掘出来的代码
现在找不到原代码地址了
LOL暂且这样吧
"""
import ctypes


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


def move(x, y):
    STD_OUTPUT_HANDLE = -11
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    dwCursorPosition = COORD()
    dwCursorPosition.X = x
    dwCursorPosition.Y = y
    ctypes.windll.kernel32.SetConsoleCursorPosition(std_out_handle, dwCursorPosition)
