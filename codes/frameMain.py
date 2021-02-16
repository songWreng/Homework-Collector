import wx
import MyFrame
from settings import *
import tkinter as tk
from tkinter import filedialog

def getTxtPath():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    return filepath


print("请选择settings所在目录")
txtpath = getTxtPath()
print("所选的设置文件的目录为:%s" % txtpath)
settings = Settings(txtpath)
settings.printAll()

app = wx.PySimpleApp()
frame = MyFrame.MyFrame(settings)
frame.Show(True)
app.MainLoop()
