from collector import *
from settings import *
import os

def main():
    txtpath = os.path.abspath(__file__).rstrip('\codes\main.py') + "\datas\settings.txt"
    settings = Settings(txtpath)
    settings.printAll()
    collector = Collector(settings)
    collector.sortFiles(settings)
    collector.printHwinf(2)
    
    ord = ''
    printMenu()
    while True:
        ord = input(">>> ")
        if ord == 'quit':
            break
        elif ord == 'sort':
            print("\n开始整理")
            collector.sortFiles(settings)
        elif ord == 'print unfinish':
            print("\n打印未完成作业同学名单")
            collector.printHwinf(0)
        elif ord == 'print finish':
            print("\n打印完成作业的好同学名单")
            collector.printHwinf(1)
        elif ord == 'print all':
            print("\n打印所有的同学信息")
            collector.printHwinf(2)
        elif ord == 'print menu':
            print("\n打印菜单")
            printMenu()
        elif ord == 'clear':
            os.system('cls')
        elif ord == 'print settings':
            print("\n打印设置信息")
            settings.printAll()
        else:
            print("\n无效命令!") 

    ord = input("是否保存日志?[y/n]: ")
    if ord in 'Yy':
        collector.printLog(settings.Datas[Get.LOG_PATH.value], 0)
        
    print("感想使用!")

def printMenu():
    print(
        "菜单\n"
        "- quit\n"
        "- sort\n"
        "- print unfinish\n"
        "- print finish\n"
        "- print all\n"
        "- print menu\n"
        "- print settings\n"
        "- clear\n"
    )
if __name__ == '__main__':
    main()

