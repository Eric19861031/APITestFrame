# -*- coding: utf-8 -*-
import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import commons
from common import configHttp as ConfigHttp

login_MDM_xls = commons.get_xls("userCase.xlsx", "login_MDM")   # 获取用例的所有参数，需要比较的返回值
localReadConfig = readConfig.ReadConfig()   # 解析初始化文件 ini
configHttp = ConfigHttp.ConfigHttp()    # 获取HTTP相关方法和参数
info = {}


@paramunittest.parametrized(*login_MDM_xls)
class LoginMDM(unittest.TestCase):
    def setParameters(self, case_name, method, accountName, password, pcSn, mainVersion,success,code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param accountName:
        :param password:
        :param pcSn:
        :param mainVersion:
        :param success:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.accountName = str(accountName)
        self.password = str(password)
        self.pcSn = str(pcSn)
        self.mainVersion = str(mainVersion)
        self.success = str(success)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+" : 测试开始前准备")

    def testLoginMDM(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commons.get_url_from_xml('Login_MDM')
        # configHttp.set_url('http://103.24.178.114:8083/nrm/operator/login?token=')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None

        # set headers
        # header = {"Content-Type": "application/json"}
        # configHttp.set_headers(header)
        print("第二步：本来需要设置头，可是这里没有token也不需要特殊设定故此不需要")

        # set json
        json = {"accountName": self.accountName,"password": self.password,"pcSn": self.pcSn,"mainVersion": self.mainVersion}
        # print(json)
        configHttp.set_json(json)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.postJson()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        if info['code'] == 0:
            # get uer token
            token_u = commons.get_value_from_return_json(info, 'member', 'token')
            # set user token to config file
            localReadConfig.set_headers("TOKEN_U", token_u)
        else:
            pass
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        commons.show_return_msg(self.return_json)
        self.assertEqual(self.info['msg'], self.msg)
        # self.assertEqual(self.info['mainVersion'], self.mainVersion)
        # self.assertEqual(self.info['success'], self.success)
        # self.assertEqual(self.info['code'], self.code)
