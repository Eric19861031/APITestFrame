# -*- coding: utf-8 -*-
import os
import unittest

import time

from common.Log import MyLog as Log
import readConfig as readConfig
import HTMLTestRunner
from common.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log() # 每运行一次，回去创建一个日志文件
        logger = log.get_logger() # 获取日志信息
        resultPath = log.get_report_path()  # 在日志文件下会生成一个报告
        on_off = localReadConfig.get_email("on_off") # 设定是否发送邮件
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt") # 定位用例清单
        self.caseFile = os.path.join(readConfig.proDir, "testCase") # 定位用例的路径
        # self.caseFile = None
        self.caseList = []  # 到时候会把用例的地址轮询到这里面
        self.email = MyEmail.get_email()    # 启动一个邮件的实例
    # 读取用例清单，将用例清单内容加进列表
    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()  # 获取一个测试套件的实例
        suite_module = []   # 套件用例模块列表

        for case in self.caseList:
            case_name = case.split("/")[-1] # 获取用例名
            print(case_name+".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)
        # 执行用例
        if len(suite_module) > 0:

            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            fp.close()
            # send test report by email
            if on_off == 'on':
                time.sleep(10)
                self.email.send_email()
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
