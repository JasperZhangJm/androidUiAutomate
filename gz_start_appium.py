# from appium import webdriver
# import gz_public
import os
import time
import subprocess


class StartAppium:
    @staticmethod
    def start_appium(host="127.0.0.1", port=4723):
        """
        启动appium服务
        :param host: appium地址
        :param port: 端口号
        :return:
        """
        netstat_info = os.popen('netstat -ano | findstr %s' % port)
        time.sleep(2)
        load_netstat_info = netstat_info.read()
        if "LISTENING" in load_netstat_info:
            print("appium服务已经启动\n：%s" % load_netstat_info)
        else:
            start_appium_cmd = 'start /b appium -a %s -p %s' % (host, port)
            print("%s at %s " % (start_appium_cmd, time.ctime()))
            subprocess.Popen(start_appium_cmd, shell=True, stdout=open('./report' + str(port) + '.log', 'a'), stderr=subprocess.STDOUT)

        '''
        desired_caps = dict(
            deviceName=gz_public.CONNECTTO,
            platformName=gz_public.gzPlatformN,
            platformVersion=gz_public.PLATFORMVER,
            appPackage=gz_public.gzAppPack,
            appActivity=gz_public.gzAppActivity,
            noReset=True,  # 如果是False的话是卸载再重装app，所以一定要指定是True
            autoGrantPermissions=True,  # 安装时自动赋予权限
            newCommandTimeout=6000,
            automationName='UiAutomator2'
        )
        
        driver = webdriver.Remote(gz_public.gzAppiumH, desired_caps, direct_connection=True)
        driver.implicitly_wait(10)
        return driver
        '''