#coding=utf-8


import time,os
import logging

#使用相对路径+绝对路径
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
log_path = PATH(os.getcwd())

class Log():

    def __init__(self,Logger=None):

        filename = 'mock'+''.join(time.strftime('%Y%m%d'))+''.join('.log') #设置log名
        self.logname =os.path.join(log_path, filename)
        self.logger = logging.getLogger(Logger)
        self.logger.setLevel(logging.DEBUG)
        #设置日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - [%(name)s] [%(levelname)s] - %(message)s')


    def output(self,level,message):
        '''
        :param level: 日志等级
        :param message: 日志需要打印的信息
        :return:
        '''

        #send logging output to a disk file
        #指定编码utf-8，防止输出中文乱码
        fh = logging.FileHandler(self.logname,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        #send logging output to streams
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level =='debug':
            self.logger.debug(message)
        elif level =='warn':
            self.logger.warning(message)
        elif level =='error':
            self.logger.error(message)

        #防止重复打印
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)

        fh.close()

    def info(self,message):
        self.output('info',message)

    def debug(self,message):
        self.output('debug',message)

    def warn(self,message):
        self.output('warn',message)

    def error(self,message):
        self.output('error',message)

    def getlog(self):
        return self.logger

