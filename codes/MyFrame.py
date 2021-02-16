import wx
import os
from settings import *

class MyFrame(wx.Frame):

	def __init__(self, settings, parent=None):

		wx.Frame.__init__(self, parent, id=-1, title='配置setting.txt',
			pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE, size=(600, 500))

		self.settings = settings
		self.pathstrs = [
			self.settings.Datas[Get.EXCEL_PATH.value],
			self.settings.Datas[Get.UNSORT_PATH.value],
			self.settings.Datas[Get.SORTED_PATH.value],
			self.settings.Datas[Get.LOG_PATH.value]
		]
		self.pathID = 0
		
		panel = wx.Panel(self) # 创建画板

		posx = 10; posy = 10; btnx = 85; btny = 30
		textCtrlx = 480

		ExcelButton = wx.Button(panel, label=u"学生信息表格", pos=(posx, posy), size=(btnx, btny))
		self.ExcelTextCtrl = wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy+2), size=(textCtrlx, -1))
		self.ExcelTextCtrl.SetValue(self.pathstrs[0])
		self.Bind(wx.EVT_BUTTON, self.ClickExcelBtn, ExcelButton)
		
		posy += (btny + 3)
		UnsortButton = wx.Button(panel, label=u"待整理文件夹", pos=(posx, posy), size=(btnx, btny))
		self.UnsortTextCtrl = wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy+2), size=(textCtrlx, -1))
		self.UnsortTextCtrl.SetValue(self.pathstrs[1])
		self.Bind(wx.EVT_BUTTON, self.ClickUnsortBtn, UnsortButton)
				
		posy += (btny + 3)
		SortedButton = wx.Button(panel, label=u"已整理文件夹", pos=(posx, posy), size=(btnx, btny))
		self.SortedTextCtrl = wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy+2), size=(textCtrlx, -1))
		self.SortedTextCtrl.SetValue(self.pathstrs[2])
		self.Bind(wx.EVT_BUTTON, self.ClickSortedBtn, SortedButton)

		posy += (btny + 3)
		LogButton = wx.Button(panel, label=u"日志文件夹", pos=(posx, posy), size=(btnx, btny))
		self.LogTextCtrl = wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy+2), size=(textCtrlx, -1))
		self.LogTextCtrl.SetValue(self.pathstrs[3])
		self.Bind(wx.EVT_BUTTON, self.ClickLogBtn, LogButton)

		# NOTE:
		posy += (btny + 3)
		wx.StaticText(panel, -1, "作业序号:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_ID_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.HW_ID_TextCtrl.SetValue(str(self.settings.Datas[Get.HW_ID.value]))

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 作业名称:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_NAME_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.HW_NAME_TextCtrl.SetValue(self.settings.Datas[Get.HW_NAME.value])

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 作业内容:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_NOTE_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.HW_NOTE_TextCtrl.SetValue(self.settings.Datas[Get.HW_NOTE.value])

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 预计作业份数:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_COUNT_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.HW_COUNT_TextCtrl.SetValue(str(self.settings.Datas[Get.HW_COUNT.value]))

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 作业命名格式:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.NAMEFORMAT_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.NAMEFORMAT_TextCtrl.SetValue(self.settings.Datas[Get.NAME_FORMAT.value])

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 学号正则表示:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.IDREGEX_TextCtrl =  wx.TextCtrl(panel, id=-1, value="", pos=(posx+btnx+4, posy), size=(textCtrlx, -1))
		self.IDREGEX_TextCtrl.SetValue(self.settings.Datas[Get.IDREGEX.value])

		posy += (btny + 3)
		wx.StaticText(panel, -1, " 作业类型:", pos=(posx, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_TYPE_Cbox = wx.ComboBox(panel, -1, "作业", pos=(posx+btnx+4, posy), size=(70,btny), choices=['实验', '作业'], style=wx.CB_DROPDOWN)

		# posy += (btny + 3)
		wx.StaticText(panel, -1, " 作业提交格式:", pos=(posx+btnx+90, posy), size=(btnx, btny), style=wx.ALIGN_RIGHT)
		self.HW_FORMAT_Cbox = wx.ComboBox(panel, -1, ".pdf", pos=(posx+2*btnx+96, posy), size=(70,btny), choices=['.pdf', '.m', '.doc', '.zip', '.rar', '.txt'], style=wx.CB_DROPDOWN)

		posy += (btny + 3)
		sureButton = wx.Button(panel, label=u"确认", pos=(posx+btnx+4, posy), size=(btnx, btny))
		self.Bind(wx.EVT_BUTTON, self.clickSurebtn, sureButton)
		
		quitButton = wx.Button(panel, label=u"取消", pos=(posx+2*btnx+96, posy), size=(btnx, btny))
		self.Bind(wx.EVT_BUTTON, self.OnCloseMe, quitButton)
		self.Bind(wx.EVT_CLOSE, self.OnCloseWIndow)


	def ClickExcelBtn(self, event):
		self.pathID = 0
		self.ChooseFilePath(None)
		self.ExcelTextCtrl.SetValue(self.pathstrs[self.pathID])

	def ClickUnsortBtn(self, event):
		self.pathID = 1
		self.ChooseDirPath(None)
		self.UnsortTextCtrl.SetValue(self.pathstrs[self.pathID])
	
	def ClickSortedBtn(self, event):
		self.pathID = 2
		self.ChooseDirPath(None)
		self.SortedTextCtrl.SetValue(self.pathstrs[self.pathID])

	def ClickLogBtn(self, event):
		self.pathID = 3
		self.ChooseDirPath(None)
		self.LogTextCtrl.SetValue(self.pathstrs[self.pathID])

	def ChooseFilePath(self, event):
		"""
		选择文件路径
		"""
		wildcard = "All files(*.*)|*.*"
		dlg = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			reponse = dlg.GetPath()
			self.pathstrs[self.pathID] = reponse
			print(reponse)
		dlg.Destroy()

	def ChooseDirPath(self, event):
		"""
		选择目录路径
		"""
		dlg = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
		if dlg.ShowModal() == wx.ID_OK:
			reponse = dlg.GetPath()
			self.pathstrs[self.pathID] = reponse
			print(reponse)
		dlg.Destroy()

	def OnCloseMe(self, event):
		self.Close(True)
	
	def OnCloseWIndow(self, envet):
		self.Destroy()
	
	def clickSurebtn(self, event):
		self.settings.Datas[Get.EXCEL_PATH.value] = self.ExcelTextCtrl.GetValue()
		self.settings.Datas[Get.UNSORT_PATH.value] = self.UnsortTextCtrl.GetValue()
		self.settings.Datas[Get.SORTED_PATH.value] = self.SortedTextCtrl.GetValue()
		self.settings.Datas[Get.LOG_PATH.value] = self.LogTextCtrl.GetValue()
		self.settings.Datas[Get.HW_ID.value] = int(self.HW_ID_TextCtrl.GetValue())
		self.settings.Datas[Get.HW_COUNT.value] = int(self.HW_COUNT_TextCtrl.GetValue())
		self.settings.Datas[Get.HW_FORMAT.value] = self.HW_FORMAT_Cbox.GetValue()
		self.settings.Datas[Get.HW_NAME.value] = self.HW_NAME_TextCtrl.GetValue()
		self.settings.Datas[Get.HW_NOTE.value] = self.HW_NOTE_TextCtrl.GetValue()
		self.settings.Datas[Get.HW_TYPE.value] = self.HW_TYPE_Cbox.GetValue()
		self.settings.Datas[Get.NAME_FORMAT.value] = self.NAMEFORMAT_TextCtrl.GetValue()	
		self.settings.Datas[Get.IDREGEX.value] = self.IDREGEX_TextCtrl.GetValue()
		self.settings.printFile(self.settings.txtpath)
		print("保存成功")
		self.settings.printAll()