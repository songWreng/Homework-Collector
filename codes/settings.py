import os
from enum import IntEnum, unique 

@unique
class Get(IntEnum):
    """settings的属性枚举"""
    EXCEL_PATH = 0      # 学生信息表格, str
    UNSORT_PATH = 1     # 待整理文件路径, str
    SORTED_PATH = 2     # 已整理文件路径, str
    LOG_PATH = 3        # 日志文件路径, str
    HW_ID = 4           # 作业序号, int
    HW_NAME = 5         # 作业名称, str
    HW_TYPE = 6         # 作业类型, str
    HW_FORMAT = 7       # 作业扩展名, list
    HW_NOTE = 8         # 作业内容, str
    HW_COUNT = 9        # 预计应收的作业份数, int
    NAME_FORMAT = 10    # 命名格式, str
    IDREGEX = 11        # 学号的正则表达式, str

class Settings():
    """
    读取settings.txt的设置信息，保存相关的设置信息的类
    """
    def __init__(self, txtpath):

        self.WorkSpacePath = os.path.dirname(__file__).rstrip('\codes')
        self.Datas = [None]*len(Get)
        self.txtpath = txtpath
        self.__readtxt__(txtpath)
        self.__setauto__()
    
    def __readtxt__(self, txtpath):
        """
        从settings.txt读取设置信息
        """
        print('\正在读取', txtpath, '...') # FIXME

        # 从txt中获取原始设置信息，均为字符串
        with open(txtpath, 'r', encoding='utf-8') as f:
            line  = f.readline()
            while line:
                if line[0] != '#' and line[0] != '\n':
                    [key, value] = line.split('=')
                    key = key.strip(' ').rstrip(' ')
                    value = value.strip(' ').rstrip('\n').rstrip(' ')
                    try:
                        self.Datas[Get[key].value] = value
                    except:
                        print("\n错误：settings.txt中的<", key, ">不合法！\ntxtpath, 失败读取!") # FIXME
                        raise(IndexError)
                line = f.readline() 
        
        # 对原始设置信息进一步处理
        self.Datas[Get.HW_ID.value] = int(self.Datas[Get.HW_ID.value])
        self.Datas[Get.HW_COUNT.value] = int(self.Datas[Get.HW_COUNT.value])
        self.Datas[Get.HW_FORMAT.value] = [c.strip().rstrip() for c in self.Datas[Get.HW_FORMAT.value].split(',')]

        print("\n成功读取", txtpath) # FIXME
    
    def __setauto__(self):
        """
        修正设置中的自动化选项
        如果 UNSORT_PATH 设置为 auto, 则默认为工作区下的unsort
        如果 LOG_PATH 设置为 auto, 则默认在工作区下的 log 的子文件夹k(k为作业次数)，（可以自动创建）
        如果 SORT_PATH 设置为 auto, 则默认在工作区下的 sort 的子文件夹第k次 （可以自动创建）
        """
        print("\n自动设置：")

        # 修正auto
        if self.Datas[Get.UNSORT_PATH.value] == 'auto':
            self.Datas[Get.UNSORT_PATH.value] = self.WorkSpacePath + '\\unsort'
            print("\t待整理文件夹:", self.Datas[Get.UNSORT_PATH.value]) # FIXME
        if not os.path.exists(self.Datas[Get.UNSORT_PATH.value]):
            print("\n错误：<", self.Datas[Get.UNSORT_PATH.value],"> 不存在！") # FIXME
            raise(ValueError)

        if self.Datas[Get.LOG_PATH.value] == 'auto':
            self.Datas[Get.LOG_PATH.value] = self.WorkSpacePath + '\log\\' + str(self.Datas[Get.HW_ID.value]) 
            print("\t日志文件夹:", self.Datas[Get.LOG_PATH.value]) # FIXME
        if not os.path.exists(self.Datas[Get.LOG_PATH.value]):
            os.makedirs(self.Datas[Get.LOG_PATH.value])
            print("\n警告：<", self.Datas[Get.LOG_PATH.value],"> 不存在！\n已自动创建log文件夹!") # FIXME

        # if self.Datas[Get.HW_ID.value] == -1:
        #     logpath = self.Datas[Get.LOG_PATH.value]
        #     logfiles = os.listdir(logpath)
        #     if logfiles:
        #         nums = [int(c) for c in logfiles]
        #         self.Datas[Get.HW_ID] = max(nums) + 1
        #     else:
        #         self.Datas[Get.HW_ID.value] = 1
        #     print("\t作业序号:", self.Datas[Get.HW_ID.value]) # FIXME


        if self.Datas[Get.SORTED_PATH.value] == 'auto':
            sortedpath = self.WorkSpacePath + '\sorted\第' + str(self.Datas[Get.HW_ID.value]) + '次'
            self.Datas[Get.SORTED_PATH.value] = sortedpath
            if not os.path.exists(sortedpath):
                os.makedirs(sortedpath)    
            print("\t输出文件:", sortedpath) # FIXME

        print("\n自动设置完成")

    def printAll(self):
        """
        打印设置信息
        """
        tmpStr = ["学生信息表格", "待整理文件路径", "已整理文件路径", 
        "日志文件路径:", "作业序号:", "作业名称:", "作业类型", 
        "作业扩展名", "作业内容", "预计收作业的份数", "命名格式", "学号正则表示"]
        print("\n设置信息如下：")
        for name, value in zip(tmpStr, self.Datas):
            print(name, ":", value, ",Type=", type(value))
        print("\n\t\t\t\t以上!")

    def printFile(self, path):
        """
        根据设置另存新的额settings未见
        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(("EXCEL_PATH=%s\n" % self.Datas[Get.EXCEL_PATH.value]))
            f.write(("UNSORT_PATH=%s\n" % self.Datas[Get.UNSORT_PATH.value]))
            f.write(("SORTED_PATH=%s\n" % self.Datas[Get.SORTED_PATH.value]))
            f.write(("LOG_PATH=%s\n" % self.Datas[Get.LOG_PATH.value]))
            
            f.write(("HW_ID=%d\n" % self.Datas[Get.HW_ID.value]))
            f.write(("HW_NAME=%s\n" % self.Datas[Get.HW_NAME.value]))
            f.write(("HW_TYPE=%s\n" % self.Datas[Get.HW_TYPE.value]))
            f.write(("HW_FORMAT=%s\n" % self.Datas[Get.HW_FORMAT.value]))
            f.write(("HW_NOTE=%s\n" % self.Datas[Get.HW_NOTE.value]))
            f.write(("HW_COUNT=%d\n" % self.Datas[Get.HW_COUNT.value]))
            f.write(("NAME_FORMAT=%s\n" % self.Datas[Get.NAME_FORMAT.value]))
            f.write(("IDREGEX=%s\n" % self.Datas[Get.IDREGEX.value]))
        print("\n完成!设置保存在", path)



