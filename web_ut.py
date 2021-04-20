# -*- coding: utf-8 -*-
# 创建时间：2021/4/18 15:15
import configparser
import os
import sys
import time
import unittest

import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


@allure.feature('Test Baidu WebUI')
class ISelenium(unittest.TestCase):
    # 读入配置文件
    def get_config(self):
        config = configparser.ConfigParser()
        # windows写法
        # config.read(os.path.join('C:', os.environ['HOMEPATH'], 'iselenium.ini'))
        # config.read(os.path.join('C:' + os.environ['HOMEPATH'], 'iselenium.ini'))
        # 在liunux中是这么写
        # config.read(os.path.join(os.environ['HOME'], 'iselenium.ini'))
        # 使用jenkins编译时，这么写：然后把配置文件放到JENKINS_HOME目录下去
        # JENKINS_HOME一般来说是：C:\Windows\System32\config\systemprofile\AppData\Local\Jenkins\.jenkins
        # config.read(os.path.join(os.environ['JENKINS_HOME'], 'iselenium.ini'))
        # 为了Jenkins构建和windows执行都可以
        # 获得当前系统的类型
        nowPlatform = sys.platform
        if nowPlatform == 'win32':
            print("这里是Windows系统:" + os.environ['HOMEPATH'])
            config.read(os.path.join('C:' + os.environ['HOMEPATH'], 'iselenium.ini'))
        elif nowPlatform == 'linux':
            print("这里是Linux系统:" + os.environ['PATH'])
            config.read(os.path.join(os.environ['PATH'], 'iselenium.ini'))
        else:
            print("这里我也不知道是哪个系统，就放在Jenkins地址下吧:" + os.environ['JENKINS_HOME'])
            config.read(os.path.join(os.environ['JENKINS_HOME'], 'iselenium.ini'))
        # try:
        #     config.read(os.path.join('C:' + os.environ['HOMEPATH'], 'iselenium.ini'))
        # except KeyError:
        #     config.read(os.path.join(os.environ['JENKINS_HOME'], 'iselenium.ini'))

        return config

    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        # 获取配置文件
        config = self.get_config()
        chrome_options = Options()
        # 获得当前系统类型
        nowPlatform = sys.platform
        if nowPlatform == 'win32':
            print("这里是Windows系统")
            # chrome_options = Options()
            # 获得配置文件中，是否需要无界面运行的参数
            using_headless = config.get('driver_win7', 'using_headless')
            if using_headless == 'no':
                print('using_headless的值为：' + using_headless + '使用无界面方式运行')
                chrome_options.add_argument("--headless")
            else:
                print('using_headless的值为：' + using_headless + '使用有界面方式运行')
            # 指定chrome浏览器的路径
            chrome_path = config.get('driver_win7', 'chrome')
            if chrome_path != 'no_need':
                chrome_options.binary_location = chrome_path
                # chrome_options.binary_location = "C:\\Users\\WJ\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
                # print('+++++++++++++++++++++' + chrome_path)
            # 启动浏览器
            chrome_driver_path = config.get('driver_win7', 'chrome_driver')
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options)
            # print("+++++++++++++++++" + chrome_driver_path)
            # self.driver = webdriver.Chrome()
        elif nowPlatform == 'linux':
            print("这里是Linux系统")
            # 禁用沙箱【不加在liunx下会报错】
            chrome_options.add_argument('--no-sandbox')
            # 获得配置文件中，是否需要无界面运行的参数
            using_headless = config.get('driver_centos7', 'using_headless')
            if using_headless == 'no':
                print('using_headless的值为：' + using_headless + '使用无界面方式运行')
                chrome_options.add_argument("--headless")
            else:
                print('using_headless的值为：' + using_headless + '使用有界面方式运行')
            # 指定chrome浏览器的路径
            chrome_path = config.get('driver_centos7', 'chrome')
            if chrome_path != 'no_need':
                chrome_options.binary_location = chrome_path
            # 启动浏览器
            self.driver = webdriver.Chrome(executable_path=config.get('driver_centos7', 'chrome_driver'),
                                           options=chrome_options)
        else:
            print("这里我也不知道是哪个系统")

        # self.driver = webdriver.Chrome(options=chrome_options)

    @allure.story('Test key word 今日头条')
    def test_webui_1(self):
        """ 测试用例1，验证'今日头条'关键词在百度上的搜索结果1
        """

        self._test_baidu('今日头条', 'test_webui_1')

    @allure.story('Test key word 王者荣耀')
    def test_webui_2(self):
        """ 测试用例2， 验证'王者荣耀'关键词在百度上的搜索结果
        """

        self._test_baidu('王者荣耀', 'test_webui_2')

    def _test_baidu(self, search_keyword, testcase_name):
        """ 测试百度搜索子函数
        :param search_keyword: 搜索关键词 (str)
        :param testcase_name: 测试用例名 (str)
        """

        self.driver.get("https://www.baidu.com")
        self.driver.maximize_window()
        print('打开浏览器，访问 www.baidu.com')
        time.sleep(5)
        assert f'百度一下' in self.driver.title

        elem = self.driver.find_element_by_name("wd")
        elem.send_keys(f'{search_keyword}{Keys.RETURN}')
        print(f'搜索关键词~{search_keyword}')
        time.sleep(5)
        self.assertTrue(f'{search_keyword}' in self.driver.title, msg=f'{testcase_name}校验点 pass')
