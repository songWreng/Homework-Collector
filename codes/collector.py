
import re
import os
from openpyxl import load_workbook
import datetime
from settings import *

class Collector():
    """
    负责作业命名和统计作业提交信息
    """
    def __init__(self, settings):
        
        self.Wb = None # 工作簿
        self.Ws = None # 工作表
        self.StudentNum = -1 # 学生总人数
        self.Names = {} # 学生姓名字典
        self.Submission = {} # 提取信息
        self.ExcelPos = {} # 学生信息在表格中的坐标
        self.EscapeDic = { # 转移字典
            'hwID': settings.Datas[Get.HW_ID.value], 
            'hwName': settings.Datas[Get.HW_NAME.value], 
            'hwType': settings.Datas[Get.HW_TYPE.value], 
            'hwFormat': '', 
            'stuName':'', 
            'stuID':''
        }
        self.IDRegexStr = settings.Datas[Get.IDREGEX.value]
        self.__readxlsx__(settings.Datas[Get.EXCEL_PATH.value], settings.Datas[Get.HW_ID.value])

        if settings.Datas[Get.HW_COUNT.value] != self.StudentNum:
            print("\n警告：设置中的预期需要收的作业(%d)与表格中的学生数目(%d)不等!" % (settings.Datas[Get.HW_COUNT.value], self.StudentNum)) # FIXME

    def __readxlsx__(self, excalpath, hwID):
        """
        读取的表格信息
        """
        try:
            self.Wb = load_workbook(excalpath)
            self.Ws = self.Wb["Sheet1"]
        except:
            print("\n错误!无法打开表格<", excalpath, ">") # FIXME
            raise(ValueError)

        self.StudentNum = len(self.Ws['A']) - 1 # 表格中的实际人数
        rows = self.Ws['A2':("B"+str(self.StudentNum + 1))]
        aimbeginCh = self.__jointChr__('B', 1, hwID, 1)
        aimEndCh = self.__jointChr__('B', 1, hwID, self.StudentNum)
        aimcols = self.Ws[aimbeginCh:aimEndCh]
        cnt = 1
        for row,aimcol in zip(rows, aimcols):
            id = str(row[0].value)
            name = row[1].value
            self.Names[id] = name
            self.Submission[id] = aimcol[0].value
            self.ExcelPos[id] = self.__jointChr__('B', 1, hwID, cnt)
            cnt = cnt + 1
    
    def __jointChr__(self, ochr, oint, dc, di):
        """
        计算、拼接表格的坐标 B2 (ochr, oint)+ (dc, di)
        """
        return chr(ord(ochr) + dc) + str(oint+di)

    def __saveExcel__(self, excelpath):
        """
        保存表格
        """
        self.Wb.save(excelpath)

    def sortFiles(self, settings):
        """
        整理unsort文件夹
        """
        unsortpath =  settings.Datas[Get.UNSORT_PATH.value]
        print("\n正在整理unosrt文件夹", unsortpath, "...") # FIXME
        try:
            unsortfiles = os.listdir(unsortpath)
        except:
            print("\n错误！unsort文件不存在!")
            raise(ValueError)

        for unsortfile in unsortfiles:
            
            islegal = True

            ID = self.extractID(unsortfile) # 提取学号信息
            if ID == '' or ID not in self.Names: # 判断学号是否合法
                print("\n警告：<%s>中包含多个或者无学号信息" % unsortfile) # FIXME
                islegal = False
            
            format = self.extraceExt(unsortfile) # 提取扩展名
            if format not in settings.Datas[Get.HW_FORMAT.value]:
                print("\n警告:<%s>的扩展名不符合设置规定" % unsortfile) # FIXME
                islegal = False
            self.EscapeDic['hwFormat'] = format # 修改转义字典
            
            if not islegal:
                print("%s存在非法设置，跳过对其处理" % unsortfile)
            else:
                newname = self.renameFile(ID, settings.Datas[Get.NAME_FORMAT.value])
                print("\n文件名修改为<", newname, ">") # FIXME        
                res = self.moveFile(
                    settings.Datas[Get.UNSORT_PATH.value], 
                    settings.Datas[Get.SORTED_PATH.value], 
                    unsortfile, newname)
                if res:
                    aimceil = self.Ws[self.ExcelPos[ID]]
                    self.Submission[ID] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    aimceil.value = self.Submission[ID]
        
        self.__saveExcel__(settings.Datas[Get.EXCEL_PATH.value])

    def extraceExt(self, unsortfile):
        """从文件名中提取出扩展名"""
        regex = re.compile(r'\..+$')
        formats =  regex.findall(unsortfile)
        if len(formats) > 1 or len(formats) == 0:
            format = ''
        else:
            format = formats[0]
        return format

    def extractID(self, unsortfile):
        """从文件名中提取出学号信息"""
        regex = re.compile(self.IDRegexStr)
        ids = regex.findall(unsortfile)
        if len(ids) > 1 or len(ids) == 0:
            id = ''
        else:
            id = ids[0]
        return id

    def renameFile(self, id, nameformat):
        """
        获取对应学号id的文件新命名
        """
        # 根据学号修改 EscapeDic 转义字典
        self.EscapeDic['stuName'] = self.Names[id]
        self.EscapeDic['stuID'] = id

        newname = nameformat
        regex = re.compile(r'\[.+?\]')
        escapewords = regex.findall(nameformat)
        for escapeword in escapewords:
            eword = escapeword.strip('[').rstrip(']')
            if eword not in self.EscapeDic:
                print("\n错误!设置的命名格式不符合法!<%s>" % eword) #FIXME
                raise(ValueError)
            newname = newname.replace("["+eword+"]", str(self.EscapeDic[eword]))        
        return newname

    def moveFile(self, unsortpath, sortedpath, oldname, newname):
        """移动文件加"""
        aimpath = sortedpath + "/" + newname
        sourcepath = unsortpath + "/" + oldname
        staypath = unsortpath + '/' + newname
        res = True
        if not os.path.exists(aimpath):
            os.rename(sourcepath, aimpath)
            print("\n <%s> 成功处理" % aimpath) # FIXME
        else:
            os.rename(sourcepath, staypath)
            print("\n 警告 <%s> 已存在 <%s>文件中，保存在原文件" % (aimpath, staypath)) # FIXME
            res = False
        return res

    def printHwinf(self, mode=0):
        """
        打印未完成(mode=0)或者完成(mode=1)作业的同学
        """
        #      01  40401001  张小三  2021-01-20 02:30:01
        print("----+---------+-------+-------------------")
        print("NO  ID        Name    Submission")
        cnt = 0
        for ID in self.Submission:
            if mode != 1 and mode != 0:
                cnt += 1
                name = self.Names[ID]
                submission = self.Submission[ID]
            elif self.Submission[ID] and mode==1:
                cnt += 1
                name = self.Names[ID]
                submission = self.Submission[ID]
            elif self.Submission[ID]==None and mode==0:
                cnt += 1
                name = self.Names[ID]
                submission = self.Submission[ID]
            else:
                continue
            
            if len(name) == 2:
                print("%-4.2d%-10.8s%-5.2s %-s" % (cnt, ID, name, submission))
            else:
                print("%-4.2d%-10.8s%-5.3s%-s" % (cnt, ID, name, submission))
        print("----+---------+-------+-------------------")
        if mode == 1:
            print("\t\t作业完成度: %d/%d" % (cnt, self.StudentNum))
        elif mode == 0:
            print("\t\t作业未完成度: %d/%d" % (cnt, self.StudentNum))
        else:
            print("\t\t总共有: %d份作业" % (self.StudentNum))

    def printLog(self, logpath, mode=0):
        """
        打印日志, mode=0未完成, mode=1完成, mode=2全部 
        """
        logtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        txtname = logtime + ".txt"
        txtpath = logpath + "\\" + txtname
        print(txtpath)

        with open(txtpath, 'w', encoding='utf-8') as f:
            f.write("----+---------+-------+-------------------\n")
            f.write("NO  ID        Name    Submission\n")
            cnt = 0
            for ID in self.Submission:
                if mode != 1 and mode != 0:
                    cnt += 1
                    name = self.Names[ID]
                    submission = self.Submission[ID]
                elif self.Submission[ID] and mode==1:
                    cnt += 1
                    name = self.Names[ID]
                    submission = self.Submission[ID]
                elif self.Submission[ID]==None and mode==0:
                    cnt += 1
                    name = self.Names[ID]
                    submission = self.Submission[ID]
                else:
                    continue
                
                if len(name) == 2:
                    tmpstr = ("%-4.2d%-10.8s%-5.2s %-s\n" % (cnt, ID, name, submission))
                else:
                    tmpstr = ("%-4.2d%-10.8s%-5.3s%-s\n" % (cnt, ID, name, submission))
                f.write(tmpstr)
            f.write("----+---------+-------+-------------------\n")
            if mode == 1:
                tmpstr = ("\t\t作业完成度: %d/%d\n" % (cnt, self.StudentNum))
            elif mode == 0:
                tmpstr = ("\t\t作业未完成度: %d/%d\n" % (cnt, self.StudentNum))
            else:
                tmpstr = ("\t\t总共有: %d份作业\n" % (self.StudentNum))
            f.write(tmpstr)

