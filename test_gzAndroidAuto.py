"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20220130
----------------------------------
"""
# from appium.webmaster.connectiontype import ConnectionType
# from selenium.webdriver.support import expected_conditions
# import pytest_repeat
import logging
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from gz_public import get_dsc
from gz_start_appium import StartAppium
import gz_public
import initPhone
import pytest
import allure
import time
from datetime import datetime

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['moto g', 'Pixel 7', 'Samsung S8', 'Galaxy S10e', 'SamsungA51', 'moto_z4']

dev_tmp = []

android_package_name = 'com.glazero.android'

for device in devices:
    tmp = get_dsc(device=device)
    dev_tmp.append(tmp)


def setup_module():
    phone_1 = dev_tmp.pop(0)
    print('phone_1: ', phone_1)
    phone_2 = dev_tmp.pop(0)
    print('phone_2: ', phone_2)

    global master, slave

    StartAppium.start_appium(port=phone_1["port"])
    time.sleep(3)
    master = webdriver.Remote("http://127.0.0.1:%s" % phone_1["port"], phone_1["des"])
    master.implicitly_wait(10)

    # 用一个手机时注释掉该段，用两个手机时打开，连同第84行
    '''
    StartAppium.start_appium(port=phone_2["port"])
    time.sleep(3)
    slave = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_2["port"], phone_2["des"])
    slave.implicitly_wait(10)
    '''

    # 当前没有网络连接，设置wifi连接
    # if master.network_connection == 0:
    # master.set_network_connection(ConnectionType.WIFI_ONLY)

    # if slave.network_connection == 0:
    # slave.set_network_connection(ConnectionType.WIFI_ONLY)

    # 检查屏幕是否点亮
    if not initPhone.isAwake():
        # 26 电源键
        initPhone.keyEventSend(26)
        # 82 解锁键 去掉密码后可以注释掉下面的code
        # initPhone.keyEventSend(82)
        # 1
        # initPhone.keyEventSend(8)
        # 2
        # initPhone.keyEventSend(9)
        # 3
        # initPhone.keyEventSend(10)
        # 4
        # initPhone.keyEventSend(11)
        # 回车键
        # initPhone.keyEventSend(66)
        # 回到桌面
        initPhone.keyEventSend(3)

    # 已安装aosu 先卸载
    if initPhone.isAppExist():
        initPhone.uninstallApp()

    # 安装aosu app
    initPhone.installApp()


def teardown_module():
    master.quit()
    # slave.quit()


@allure.feature('登录模块')
class TestGzLogin(object):
    @staticmethod
    def setup_method():
        if master.current_activity != ".SplashActivity":
            # appium 1.22.2的用法
            # master.launch_app()
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)

    @allure.story('用户名和密码输入框右侧的关闭按钮和显示/隐藏按钮')
    def test_gzLoginClearShowHide(self):
        with allure.step('step1: 在splash页，点击 登录 按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

        with allure.step('step2: 输入用户名'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].clear()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].click()
            master.implicitly_wait(10)
            inputText = gz_public.randomEmail()
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].send_keys(inputText)
            master.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，邮箱地址
        # 验证输入的内容正确
        assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].text == inputText

        with allure.step('step3: 点击 用户名输入框 右侧的清除按钮‘X’'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_delete").click()
            master.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/textinput_placeholder").text == ''

        with allure.step('step4: 输入密码'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].clear()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].click()
            master.implicitly_wait(10)
            randomText = inputText.split('@')[0]
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].send_keys(randomText)
            master.implicitly_wait(10)

        # 不能隐藏键盘，因为键盘收起后输入框带有默认的提示文案，例如，密码
        # 验证输入的内容正确
        assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step5: 点击 密码输入框 右侧的显示按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_pwd_visible").click()
            master.implicitly_wait(10)

        # 验证输入的内容正确，因为点击两个按钮后没有变化，所以暂时先这样断言，后续跟开发沟通，区分一下这两个按钮
        assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].text == randomText

        with allure.step('step6: 点击 密码输入框 右侧的清除按钮‘X’'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_delete").click()
            master.implicitly_wait(10)

        # 验证 清除后的输入框为空
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/textinput_placeholder").text == ''

        # 隐藏键盘
        master.hide_keyboard()

        # 点击 右上角的关闭按钮
        master.find_element(AppiumBy.ID, "com.glazero.android:id/img_title_close").click()
        master.implicitly_wait(10)

        # 回到 splash页面，断言登录和创建账号按钮（不断言文本，因为跟语言变化）
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_create_account")

    @allure.story('输入用户名和密码登录aosu app')
    def test_gzLogin(self, user_name=gz_public.email, pass_word=gz_public.pwd, region=gz_public.REGION):
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.android.permissioncontroller:id/permission_message") is True:
            # 点击弹窗中 允许 按钮
            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="%s"]' % '允许').click()
            master.implicitly_wait(10)

        # 点击 aosu 图标7次，在地区列表中出现中国
        for ii in range(1, 8):
            master.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")[0].click()
            master.implicitly_wait(1)

        with allure.step('step1：在splash页，点击 登录 按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

        with allure.step('step2：输入用户名'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].clear()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].click()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].send_keys(user_name)

        # 输入完成后隐藏键盘
        master.hide_keyboard()

        with allure.step('step3: 输入密码'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].clear()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].click()
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[1].send_keys(pass_word)

        # 输入完成后隐藏键盘
        master.hide_keyboard()

        with allure.step('step4：选择地区'):
            # 如果默认是指定的地区，那么就直接点击登录
            if master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[2].text[-3:] == region:
                time.sleep(1)
            else:
                # 如果默认不是指定的地区，那么就在地区列表中选择
                master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[2].click()
                master.implicitly_wait(10)
                master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % region)
                master.implicitly_wait(10)
                master.find_element(AppiumBy.XPATH,
                                    '//android.widget.TextView[@text="%s"]' % region).click()  # 此时只能写类名
                master.implicitly_wait(10)
        # 点击登录按钮之前截图
        time.sleep(3)
        ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        master.save_screenshot('./report/login_%s.png' % ts)
        master.implicitly_wait(10)

        with allure.step('step5：点击 登录 按钮'):
            allure.attach.file("./report/login_%s.png" % ts, name="登录页面",
                               attachment_type=allure.attachment_type.JPG)
            master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
            master.implicitly_wait(10)

        # 点击登录按钮之后即进入首页后截图截图
        time.sleep(5)
        master.save_screenshot('./report/homePage.png')
        master.implicitly_wait(10)

        with allure.step('step6: 登录成功'):
            allure.attach.file("./report/homePage.png", name="登陆成功 进入首页",
                               attachment_type=allure.attachment_type.JPG)

        # 登录后进入首页，有可能会弹出智能提醒弹窗，发现后点击“知道了”关闭弹窗
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 登录后进入首页，有可能会弹出低电量的弹窗，发现后点击“知道了”关闭弹窗
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/btn_dialog_confirm") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_dialog_confirm").click()
            master.implicitly_wait(10)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_ad") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
            master.implicitly_wait(10)

        # 没有设备的情况下启动app后会进入select model页面，兼容该页面，点击返回<，回到首页
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/tv_title_string") is True:
            if master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Select Model':
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_back').click()
                master.implicitly_wait(10)

        # 断言是否进入首页，关键元素是：菜单按钮、logo、添加设备按钮、设备tab、回放tab、在线客服tab
        # 20230509：以下图标在1.11.18版本中已经发生变化
        assert master.current_activity in (".main.MainActivity", ".account.login.LoginActivity")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")
        # 20230509：这个图标没有了
        # assert master.find_element_by_id("com.glazero.android:id/img_logo")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_add_device")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")
        assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/img_tab_playback")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_service")

    @staticmethod
    def teardown_method():
        # appium 1.22.2的用方法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)


@allure.feature('添加设备-配网')
class TestAddDevices(object):
    """
    前提：
    1、执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    2、登录前先要启动app
    3、那么就要使用setup_class
    """

    @staticmethod
    def setup_class():
        # appium1.22.2的用法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)
        # appium1.22.2的用法
        # master.launch_app()
        master.activate_app(android_package_name)
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.isAwake():
            # 26 电源键
            initPhone.keyEventSend(26)
            time.sleep(1)

        # 不在首页的话 启动一下app
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            # appium1.22.2的用法
            # master.launch_app()
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
            time.sleep(5)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_ad") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
            master.implicitly_wait(10)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(5)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_ad") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
            master.implicitly_wait(10)

    @staticmethod
    def teardown_method(self):
        # 调用解绑接口，默认是中国区‘api-cn.aosulife.com’
        # gz_public._unbind('V8P1AH110002353', 1, 1)
        # 335
        gz_public._unbind('C2E2BH110000278', 1, 1)
        # 337
        # gz_public._unbind('C2E2BH110000233', 1, 1)
        # C6SP 基站
        # gz_public._unbind('H1L2AH110000650', 1, 1)
        # time.sleep(2)

        # 如果绑定失败的话，会停留在失败页面，每次执行完成后要回到首页
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            if master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_tip').text == 'Connection failed':
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)

        # 接口解绑成功后，再次绑定时，客户端提示：设备被其他账号绑定，但实际上绑定成功的情况，所以等待20秒
        # time.sleep(20)

        # c2e特殊场景验证，等待1小时后进行绑定
        # 强制等待时间过程driver会断开
        # time.sleep(600)
        '''
        for _i in range(1, 2):
            time.sleep(10)
            master.find_element_by_id('com.glazero.android:id/img_tab_device').click()
        '''

    @allure.title('V8P 绑定-解绑')
    @allure.story('用户循环测试V8P的绑定和解绑')
    def test_addV8P(self, ssid='11111111', pwd='12345678'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择V8P'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Pro · V8P"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：点击continue'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step4：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step5：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step7：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step8：如果弹出wifi权限弹窗则给予权限'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                if master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_confirm').text == 'GO SETTINGS':
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_confirm').click()
                    master.implicitly_wait(10)

                if master.find_element(AppiumBy.ID,
                                       'com.android.permissioncontroller:id/permission_allow_foreground_only_button').text == 'Allow only while using the app':
                    master.find_element(AppiumBy.ID,
                                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
                    master.implicitly_wait(10)

        with allure.step('step9：输入ssid和pwd'):
            # 先清除ssid
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].clear()
            # 第2次执行的时候会带ssid和pwd信息，所以不能用文本去识别
            # master.find_element_by_xpath('//android.widget.EditText[@text="Wi-Fi Name"]').clear()
            master.implicitly_wait(10)
            # 再输入ssid
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].send_keys(ssid)
            master.implicitly_wait(10)

            # 先清除pwd
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].clear()
            master.implicitly_wait(10)
            # 再输入pwd
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].send_keys(pwd)
            master.implicitly_wait(10)

            # 点击 下一步
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step10：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step11：继续点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step12：校验二维码页面生成成功'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Scan QR Code'
                master.implicitly_wait(10)

            # 如果二维码生成失败，点击页面中的Refresh
            if gz_public.isElementPresent(driver=master, by='id',
                                          value='com.glazero.android:id/tv_scan_code_load_retry') is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_scan_code_load_retry').click()
                master.implicitly_wait(10)

            # 二维码生成成功后，Iheard the “beep” sound 按钮会高亮
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').is_enabled() is True

        with allure.step(
                'step13：等待配网成功页面出现，超时时间是7分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            WebDriverWait(master, timeout=420, poll_frequency=2).until(
                lambda x: x.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Connected successfully"]'))
        # 出现后点击下一步
        master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn').click()
        master.implicitly_wait(10)

        # 进入引导页面，引导页面弹出较慢，等待5秒
        time.sleep(5)
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/tv_title_string"):
            if master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Final Steps':
                # 关闭引导页面
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)
                # 点击 YES
                master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="YES"]').click()
                master.implicitly_wait(10)

        # 验证回到了首页
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_logo")

        '''
        with allure.step('绑定失败页面'):
            assert master.find_element_by_xpath('//android.widget.TextView[@text="Connection failed"]')
            assert master.find_element_by_id('com.glazero.android:id/btn').text == 'RECONNECT'
        '''

    def test_addV8S(self):
        pass

    @allure.title('C2E 绑定-解绑')
    @allure.story('用户循环测试C2E的绑定和解绑，每次绑定间隔1个小时')
    def test_addC2E(self, ssid='11111111-5g', pwd='12345678'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择C2E'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="P1"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：弹出照相机权限后点击cancel'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_cancel').click()
            master.implicitly_wait(10)

        with allure.step('step4：点击Use other methods'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_other_way').click()
            master.implicitly_wait(10)

        with allure.step('step5：点击continue'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击continue'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step7：如果弹出wifi权限弹窗则给予权限'):
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/btn_dialog_confirm") is True:
                if master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_confirm').text == 'GO SETTINGS':
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_confirm').click()
                    master.implicitly_wait(10)

                if master.find_element(AppiumBy.ID,
                                       'com.android.permissioncontroller:id/permission_allow_foreground_only_button').text == 'Allow only while using the app':
                    master.find_element(AppiumBy.ID,
                                        'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
                    master.implicitly_wait(10)

        with allure.step('step8：输入ssid和pwd'):
            # 先清除ssid
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].clear()
            master.implicitly_wait(10)
            # 再输入ssid
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].send_keys(ssid)
            master.implicitly_wait(10)

            # 先清除pwd
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].clear()
            master.implicitly_wait(10)
            # 再输入pwd
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].send_keys(pwd)
            master.implicitly_wait(10)

            # 点击 下一步
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/next_step').click()
            master.implicitly_wait(10)

        with allure.step('step9：校验二维码页面生成成功'):
            # 二维码页面有唯一的标识：
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/lottie_guide_scan_qr_code") is True:
                assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Scan QR Code'
                # 进入二维码页面后先截图
                ts_qr = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/qr_code_%s.png' % ts_qr)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/C2E/qr_code_%s.png" % ts_qr, name="QR code",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

            # 如果二维码生成失败，点击页面中的Refresh
            if gz_public.isElementPresent(driver=master, by='id',
                                          value='com.glazero.android:id/tv_scan_code_load_retry') is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_scan_code_load_retry').click()
                master.implicitly_wait(10)

        with allure.step(
                'step10：等待配网成功页面出现，超时时间是7分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            try:
                WebDriverWait(master, timeout=420, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.XPATH,
                                             '//android.widget.TextView[@text="Connected successfully"]'))
            except TimeoutException:
                logging.error('绑定失败')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C2E/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)
            else:
                logging.info('绑定成功')
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C2E/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # with allure.title('step11：绑定成功后点击 下一步'):
                # 出现后点击下一步
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn').click()
                master.implicitly_wait(10)

                # 进入引导页面，引导页面弹出较慢，等待5秒
                time.sleep(4)
                # with allure.title('step12：关闭引导页面回到首页'):
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/tv_title_string") is True:
                    if master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title_string').text == 'Final Steps':
                        # 关闭引导页面
                        master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_close').click()
                        master.implicitly_wait(10)

                        # 点击 YES
                        master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="YES"]').click()
                        master.implicitly_wait(10)

                        # 验证回到了首页
                        time.sleep(2)
                        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")
                        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_logo")

    @allure.title('C6SP基站绑定解绑')
    @allure.story('C6SP基站绑定后涂鸦状态和aosu状态不一致，涂鸦状态是离线，aosu状态是在线，等待一段时间后状态仍然不同步')
    def test_addC6SP_station(self, ssid='11111111-5g', pwd='12345678', home_base_sn='H1L2AH110000650'):
        with allure.step(
                'step1：点击右上角的+号，开始执行时间为：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_add_device').click()
            master.implicitly_wait(10)

        with allure.step('step2：选择c6sp套装'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Max/Pro\nSystem"]').click()
            master.implicitly_wait(10)

        with allure.step('step3：弹出照相机权限后点击cancel'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_dialog_cancel').click()
            master.implicitly_wait(10)

        with allure.step('step4：点击Use other methods'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_other_way').click()
            master.implicitly_wait(10)

        with allure.step('step5：点击continue'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step6：继续点击continue'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step7：继续点击continue'):
            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="CONTINUE"]').click()
            master.implicitly_wait(10)

        with allure.step('step8：等待基站SN出现后，选择基站的SN'):
            try:
                WebDriverWait(master, timeout=30, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % home_base_sn))
            except TimeoutException:  # 此处不能写NoSuchElementException:
                logging.error('没有找到要绑定的基站sn: %s' % home_base_sn)
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 没有找到待绑定的sn可能是因为没有解绑，在这里解绑一下，保证后面步骤的运行
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('找到了要绑定的基站sn: %s' % home_base_sn)
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 出现后点击SN
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % home_base_sn).click()
                master.implicitly_wait(10)

        with allure.step('step9：跳转到Name Your HomeBase页面后，点击continue'):
            try:
                WebDriverWait(master, timeout=30, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/subtitle'))

            except TimeoutException:
                logging.error('没有找到Name Your HomeBase这个元素')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 虽然绑定失败了，解绑一下，为下一次绑定做好准备，以免提示已绑定
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('已经跳转到了Name Your HomeBase')
                master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="CONTINUE"]').click()
                master.implicitly_wait(10)

        with allure.step(
                'step10：跳转到绑定成功页面，超时时间是5分钟，每2秒检查一次页面，结束时间为：%s' % time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())):
            try:
                WebDriverWait(master, timeout=300, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/subtitle'))
            except TimeoutException:
                logging.error('绑定失败')
                ts_fail = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/fail_%s.png' % ts_fail)
                time.sleep(3)
                allure.attach.file("./report/C6SP/fail_%s.png" % ts_fail, name="fail",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 虽然绑定失败了，解绑一下，为下一次绑定做好准备，以免提示已绑定
                gz_public._unbind(home_base_sn, 1, 1)
                time.sleep(3)
            else:
                logging.info('绑定成功')
                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 点击右上角的关闭X按钮，回到首页
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_title_close').click()
                master.implicitly_wait(10)
                gz_public.swipe_down(driver=master)
                time.sleep(3)

                ts_success = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6SP/success_%s.png' % ts_success)
                time.sleep(3)
                allure.attach.file("./report/C6SP/success_%s.png" % ts_success, name="success",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 等待1分钟后再查询涂鸦状态，保证有充分的时间设备在涂鸦端上线
                time.sleep(60)

                # 绑定成功后，检查设备的涂鸦状态是否为在线，如果涂鸦端不在线，问题复现，退出pytest
                rsp = gz_public.aosu_admin_get_dev_info(home_base_sn)
                logging.info("aosu状态为：" + str(rsp.json()['data']['list'][0]['online']))
                logging.info("tuya状态为：" + str(rsp.json()['data']['list'][0]['tuyayOnline']))
                print("aosu状态为：", rsp.json()['data']['list'][0]['online'])
                print("tuya状态为：", rsp.json()['data']['list'][0]['tuyayOnline'])
                if rsp.json()['data']['list'][0]['tuyayOnline'] is False:
                    # pytest.exit('涂鸦在线，测试在这种情况下，是否执行teardown的内容   ---   结果是执行')
                    pytest.exit('绑定完成1分钟后查询涂鸦状体为离线，问题复现，终止执行pytest，请查看固件日志！')
                else:
                    # 绑定成功后，涂鸦状态为在线，那么就解绑该设备
                    gz_public._unbind(home_base_sn, 1, 1)
                    time.sleep(3)

    @staticmethod
    def teardown_class():
        # appium 1.22.2的用方法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)


@allure.feature('用户中心模块')
class TestUserCenter(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        # appium1.22.2的用法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)
        # appium1.22.2的用法
        # master.launch_app()
        master.activate_app(android_package_name)
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @allure.story('修改登录密码')
    def test_changePassword(self, old_pass_word=gz_public.pwd, new_pass_word='Qwe101010'):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 账号管理'):
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/tv_menu_item_name')[0].click()
            master.implicitly_wait(10)

        with allure.step('step3：点击 修改密码'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/rl_reset_password_container').click()
            master.implicitly_wait(10)

        assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').is_enabled() is False

        with allure.step('step4：点击密码输入旧密码'):
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].click()
            master.implicitly_wait(10)

            # 旧密码
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[0].send_keys(old_pass_word)
            master.implicitly_wait(10)

            master.hide_keyboard()

        with allure.step('step5：点击新密码输入新密码'):
            # 新密码
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].click()
            master.implicitly_wait(10)

            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[1].send_keys(new_pass_word)
            master.implicitly_wait(10)
            master.hide_keyboard()

        with allure.step('step6：点击重新输入新密码'):
            # 确认新密码
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[2].click()
            master.implicitly_wait(10)

            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/edit_text')[2].send_keys(new_pass_word)
            master.implicitly_wait(10)
            master.hide_keyboard()

        assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').is_enabled() is True

        with allure.step('step7：点击 更新密码 按钮'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        with allure.step('step8：点击 返回登录 按钮'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn').click()
            master.implicitly_wait(10)

        # 改回原密码，默认_region='CN', country_code='86'，如果换区的话需要传不同的参数
        gz_public.change_password(gz_public.change_pwd_to, gz_public.pwd, gz_public.email, gz_public._type,
                                  gz_public.gzHostCnTmp)

        # 密码复原后再回到登录状态
        TestGzLogin.test_gzLogin(self, gz_public.email, gz_public.pwd)

    @allure.story('分享设备')
    def test_shareDevice(self):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 用户分享'):
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/tv_menu_item_name')[1].click()
            master.implicitly_wait(10)

        with allure.step('step3：点击 分享设备'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_share_device').click()
            master.implicitly_wait(10)

        with allure.step('step4：选择设备，例如第一个设备'):
            master.find_elements(AppiumBy.ID, 'com.glazero.android:id/iv_device_icon')[0].click()
            master.implicitly_wait(10)

        with allure.step('分享的邮箱地址'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/et_share_user_email').click()
            master.implicitly_wait(10)
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/et_share_user_email').send_keys(
                gz_public.home_user)
            master.implicitly_wait(10)
            master.hide_keyboard()

        # 选中设备并填写邮箱后，页面底部按钮变成高亮可以点击
        assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_share').is_enabled() is True

        with allure.step('点击 分享 按钮'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_share').click()
            master.implicitly_wait(10)

        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_prompt_image"):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_share_management').click()
            master.implicitly_wait(10)

    @allure.story('退出')
    def test_logOut(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

        # 断言 进入了个人中心菜单
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon")
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击 菜单中的退出登录项'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/tv_menu_item_name")[7].click()
            master.implicitly_wait(10)

        with allure.step('step3: 点击 弹窗中的确认按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_dialog_confirm").click()
            master.implicitly_wait(10)

        # 断言 登录页面元素，退出登录后，该页面显示登录的邮箱和地区，并且登录按钮置灰不可点击
        assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[0].text == gz_public.email
        master.implicitly_wait(10)
        assert gz_public.REGION in master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[2].text
        master.implicitly_wait(10)
        assert master.find_element(AppiumBy.ID, "com.glazero.android:id/button").is_enabled() is False

    @staticmethod
    def teardown_class():
        # appium 1.22.2的用方法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)


@allure.feature('设备列表/首页 模块')
class TestDeviceList(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        # appium1.22.2的用法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)
        # appium1.22.2的用法
        # master.launch_app()
        master.activate_app(android_package_name)
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.isAwake():
            # 26 电源键
            initPhone.keyEventSend(26)
            time.sleep(1)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

    @staticmethod
    def teardown_method(self):
        pass

    @allure.title('C2E校准')
    @allure.story('C2E重复校准是否会出现问题')
    def test_C2E_Calibrate(self, dev_name='IndoorCam'):
        # 在首页的话执行step1-3
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/img_menu") is True:
            with allure.step('step1: 在设备列表中滑动找到C2E设备（默认名字是IndoorCam，可在参数中修改名字）'):
                master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s")).scrollToEnd(10,5)' % dev_name)
                master.implicitly_wait(10)

            with allure.step('step2: 点击设备名称，例如，IndoorCam'):
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
                master.implicitly_wait(10)
                time.sleep(3)  # 等待开流页面加载完成

            with allure.step('step3：点击Holder'):
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Holder"]').click()
                master.implicitly_wait(10)
                time.sleep(2)  # 等待Holder菜单加载完成

        # 如果停留在校准页面，那么就直接点击校准按钮，执行step4-5
        if gz_public.isElementPresent(driver=master, by="id",
                                      value="com.glazero.android:id/btn_calibration") is True:
            with allure.step('step4：点击Calibrate'):
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Calibrate"]').click()
                master.implicitly_wait(10)
                time.sleep(1)

                # 点击校准后，有可能会弹出提示弹窗（turn on the tracking, and the camera will follow the moving object），发现后点击“GOT
                # IT”，关闭弹窗
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/positive_btn") is True:
                    master.find_element(AppiumBy.ID, "com.glazero.android:id/positive_btn").click()
                    master.implicitly_wait(10)

                # 检验校准过程中的状态
                WebDriverWait(master, timeout=30, poll_frequency=1).until(
                    lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/pb_calibtating'))
                # master.find_element_by_xpath('//android.widget.ProgressBar[@index=3]')
                # 添加日志
                logging.info('校准中')
                # 添加截图
                calibrating = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/calibrating_%s.png' % calibrating)
                time.sleep(3)
                allure.attach.file("./report/C2E/calibrating_%s.png" % calibrating, name="calibrating",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

            with allure.step('step5：等待校准完成，校准按钮变成初始状态'):
                # 等待校准过程中的图标消失
                WebDriverWait(master, timeout=50, poll_frequency=1).until_not(
                    lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/pb_calibtating'))
                # 添加截图
                calibrate_after = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C2E/calibrate_after_%s.png' % calibrate_after)
                # 添加日志
                logging.info('校准完成')
                time.sleep(3)
                allure.attach.file("./report/C2E/calibrate_after_%s.png" % calibrate_after, name="calibrate_after",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

    @staticmethod
    def teardown_class():
        pass
        # master.close_app()
        # master.implicitly_wait(10)

@allure.feature('首页模块')
class TestHomePage(object):
    @staticmethod
    def setup_method():
        """
        # 如果崩了就再启动app
        if master.current_activity != ".SplashActivity":
            master.launch_app()
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
        """
        # 如果不在首页就按手机的返回键，直到回到首页
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_menu") is False:
            initPhone.keyEventSend(4)
            time.sleep(2)
            # 验证当前设备,未进入免打扰状态

    @allure.story('首页 设备名称')
    def test_dev_name(self):
        with allure.step('step1: 获取首页设备名称'):
            # 定位到首页所有设备的名称
            device_name_list = master.find_elements(AppiumBy.ID, "com.glazero.android:id/device_name")
            for element in device_name_list:
                print(element.text)

                # 如果有两台设备,取消下面的代码的注释
                # device_name_list = master.find_elements(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze")[1].click()

                # assert print(
                #     master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '免打扰')

                # for element in device_snooze_list:
                #     element_count = element.size
                #     print(element_count)

                # for element in device_name_list:
                #     print(element.text)

                # # 父子节点定位,当该元素无法唯一定位时,可以通过此方式来准确定位
                # child_elemnts = master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'resuandroid.widget.FrameLayout' and @index= '1']")
                #
                # master.find_element(AppiumBy.XPATH,
                #                     "//*[@resource-id='com.glazero.android:id/device_name' and @text = '家庭娱乐室']")
                # master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").click()
                # master.implicitly_wait(10)

    @allure.story('首页 免打扰')
    def test_snooze(self, ):
        # with allure.step('step1: 获取当前首页显示 免打扰按钮 的设备数量'):
        #     # 定位首页一屏显示了 免打扰按钮 的设备数量，未显示 免打扰按钮 的设备 不在计数范围内。如：当首页绑定有5台设备,但是有2台设备能显示出 免打扰 按钮,那么当前首页显示 免打扰的设备数量 就是 2
        #     device_snooze_list = master.find_elements(AppiumBy.ID,
        #                                               "com.glazero.android:id/tv_device_snooze")
        #     device_snooze_count: int = len(device_snooze_list)
        #     # 当前页面显示的所有设备都在进行 免打扰 用例测试
        #     i = 0
        #     while i < device_snooze_count:
        #         # 循环次数 小于等于当前页面显示的设备数时,执行 免打扰 测试用例
        with allure.step('step0: 初始化设备为未设置免打扰状态'):
            if master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '已休眠':
                # 如果设备处于 已休眠 状态,先结束该状态,恢复到未设置免打扰.
                master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").click()
                master.implicitly_wait(10)
                # 点击 终止休眠 按钮
                master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_stop_snooze").click()
                time.sleep(10)
                # 可以加一个强制 下滑刷新 操作,让 免打扰 的状态更新
                # gz_public.swipe_down(driver=master)
                # assert print(
                #     master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '免打扰')

        with allure.step('step1: 设置免打扰为4小时'):
            #  如果设备是 未设备免打扰状态，则点击免打扰按钮，执行测试
            with allure.step('step1-1: 如果设备未设置免打扰，则点击免打扰按钮'):
                if master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '免打扰':
                    master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").click()
                    master.implicitly_wait(10)
                    # 判断 保存设置 按钮,置灰,不可点击
                    button = master.find_element(AppiumBy.ID, "com.glazero.android:id/button")
                    # 如果 保存设置 按钮,可点击且可见
                    if button.is_enabled() and button.is_displayed():
                        print("保存按钮 可点击")
                    else:
                        print("保存按钮 不可点击")

            with allure.step('step1-2: 分别将时间进度拖动到 30分钟、1小时、2小时、3小时、4小时 位置'):
                # 获取进度条元素 的左上角坐标
                sb_seek_bar = master.find_element(AppiumBy.ID, "com.glazero.android:id/sb_seek_bar")
                sb_seek_bar_location = sb_seek_bar.location
                # 获取进度条元素 尺寸大小
                sb_seek_bar_size = sb_seek_bar.size
                # 进度条上 0分钟 位置坐标
                x1 = sb_seek_bar_location['x']
                y1 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_0min = (x1, y1)
                # 进度条上 30分钟 位置坐标
                x2 = sb_seek_bar_location['x'] + 0.2 * sb_seek_bar_size["width"]
                y2 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_30min = (x2, y2)
                # 进度条上 1小时 位置坐标
                x3 = sb_seek_bar_location['x'] + 0.4 * sb_seek_bar_size["width"]
                y3 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_1h = (x3, y3)
                # 进度条上 2小时 位置坐标
                x4 = sb_seek_bar_location['x'] + 0.6 * sb_seek_bar_size["width"]
                y4 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_2h = (x4, y4)
                # 进度条上 3小时 位置坐标
                x5 = sb_seek_bar_location['x'] + 0.8 * sb_seek_bar_size["width"]
                y5 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_3h = (x5, y5)
                # 进度条上 4小时 位置坐标
                x6 = sb_seek_bar_location['x'] + sb_seek_bar_size["width"]
                y6 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                sb_seek_bar_coordinate_4h = (x6, y6)

                # 滑动进度条 从 0min - 30min , 选择 30min
                master.swipe(x1, y1, x2, y2)
                # 滑动进度条 从 0min - 1h, 选择 1h
                master.swipe(x1, y1, x3, y3)
                # 滑动进度条 从 0min - 2h, 选择 2h
                master.swipe(x1, y1, x4, y4)
                # 滑动进度条 从 0min - 3h, 选择 3h
                master.swipe(x1, y1, x5, y5)
                # 滑动进度条 从 0min - 4h, 选择 4h
                master.swipe(x1, y1, x6, y6)

            with allure.step('step1-3: 点击 保存设置 按钮'):
                # 点击 保存设置 按钮后,页面保存成功,自动返回到首页.
                master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
                time.sleep(10)
                # 验证首页中当前设备,进入 已休眠 状态
                assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '已休眠'

                # 截一张图
                start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C4L/start_flow_%s.png' % start_flow)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/C4L/start_flow_%s.png" % start_flow, name="start flow",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

        with allure.step('step2: 将免打扰时间由4小时改为2小时'):
            if master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '已休眠':
                with allure.step('step2-1: 点击首页设备左下角的 已休眠 按钮'):
                    master.find_element(AppiumBy.ID,
                                        "com.glazero.android:id/tv_device_snooze").click()
                    master.implicitly_wait(10)

                with allure.step('step2-2: 分别将时间进度条拖动到 1小时、2小时 位置'):
                    # 获取进度条元素 的左上角坐标
                    sb_seek_bar = master.find_element(AppiumBy.ID,
                                                      "com.glazero.android:id/sb_seek_bar")
                    sb_seek_bar_location = sb_seek_bar.location
                    # 获取进度条元素 尺寸大小
                    sb_seek_bar_size = sb_seek_bar.size
                    # 进度条上 30分钟 位置坐标
                    x1 = sb_seek_bar_location['x']
                    y1 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                    sb_seek_bar_coordinate_30min = (x1, y1)
                    # 进度条上 1小时 位置坐标
                    x2 = sb_seek_bar_location['x'] + 0.25 * sb_seek_bar_size["width"]
                    y2 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                    sb_seek_bar_coordinate_1h = (x2, y2)
                    # 进度条上 2小时 位置坐标
                    x3 = sb_seek_bar_location['x'] + 0.5 * sb_seek_bar_size["width"]
                    y3 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                    sb_seek_bar_coordinate_2h = (x3, y3)
                    # 进度条上 3小时 位置坐标
                    x4 = sb_seek_bar_location['x'] + 0.75 * sb_seek_bar_size["width"]
                    y4 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                    sb_seek_bar_coordinate_3h = (x4, y4)
                    # 进度条上 4小时 位置坐标
                    x5 = sb_seek_bar_location['x'] + sb_seek_bar_size["width"]
                    y5 = sb_seek_bar_location['y'] + 0.5 * sb_seek_bar_size["height"]
                    sb_seek_bar_coordinate_4h = (x5, y5)

                    # 滑动进度条 从 30min - 1h , 选择 1h
                    master.swipe(x1, y1, x2, y2)
                    # 滑动进度条 从 1h - 2h, 选择 2h
                    master.swipe(x1, y1, x3, y3)

                with allure.step('step2-3: 点击 保存设置 按钮'):
                    # 点击 保存设置 按钮后,页面保存成功,自动返回到首页.
                    master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
                    time.sleep(10)
                    # 验证首页中当前设备,进入 已休眠 状态
                    assert master.find_element(AppiumBy.ID,
                                               "com.glazero.android:id/tv_device_snooze").text == '已休眠'

        with allure.step('step3: 取消休眠'):
            if master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").text == '已休眠':
                master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_device_snooze").click()
                master.implicitly_wait(10)
                # 点击 终止休眠 按钮
                master.find_element(AppiumBy.ID,
                                    "com.glazero.android:id/btn_stop_snooze").click()
                time.sleep(10)


@allure.feature("开流专项")
class TestOpenFlow(object):
    """
    20230424 zhang jia min
    开流专项：多次开流、长时间开流
    设备：V8S C2E
    手机：三星A51
    前提：
    1、执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    2、登录前先要启动app
    3、那么就要使用setup_class
    """
    fail_flag = 0

    # 在pytest中不能使用__init__(self, dev_name)方法，所以在setup_method中采用全局变量的方式获取设备名称
    @staticmethod
    def setup_class():
        # appium1.22.2的用法
        # master.close_app()
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)
        # appium1.22.2的用法
        # master.launch_app()
        master.activate_app(android_package_name)
        master.implicitly_wait(10)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if not gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu"):
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

    @staticmethod
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.isAwake():
            # 26 电源键
            initPhone.keyEventSend(26)
            time.sleep(1)

        # 进入首页后检查，是否有智能提醒弹窗button-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 进入首页后检查，是否有低电量提醒弹窗-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/btn_dialog_confirm") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        '''

        # 不在首页的话 启动一下app
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            # appium1.22.2的用法
            # master.launch_app()
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
            time.sleep(3)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

        # 进入首页后检查，是否有智能提醒弹窗button-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 进入首页后检查，是否有低电量提醒弹窗-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/btn_dialog_confirm") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_ad") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
            master.implicitly_wait(10)

        # 如果出现了固件升级的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/tv_dialog_ota_prompt_title") is True:
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '取消').click()
            master.implicitly_wait(10)

        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        '''

    @allure.title('V8P 多次开流')
    @allure.story('用户循环测试V8P的开流-关流，即多次开流')
    def test_v8p_open_flow(self, dev_name=gz_public.get_device_name(model='V8S')):
        """
        :前提条件：① 账号下要绑定V8P设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        """
        # 获取v8p设备的名字
        print("找到的设备名称是：", dev_name)

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，v8p'):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2: 点击前面拿到的设备名称，例如，可视门铃Pro'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step3: 进入指定设备的开流页面后开流60秒，开始时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                   time.localtime())):
            # 如果出现了引导蒙层，点击 知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_live_play_guide_next") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_live_play_guide_next").click()
                master.implicitly_wait(10)

            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/bt_play_retry") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/bt_play_retry').click()
                master.implicitly_wait(10)

            # 开流开始后 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/start_flow_%s.png" % start_flow, name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 开流开始，大概60秒
            for ii in range(1, 3):
                # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
                # 排除在开流阶段的网络波动导致开流中断的情况，如果在结束时仍为：刷新重试，那么认为开流失败。
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/bt_play_retry") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/bt_play_retry').click()
                    master.implicitly_wait(10)

                # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/liveplay_power_prompt_got_it').click()
                    master.implicitly_wait(10)

        with allure.step('step4：点击页面左上角的 返回，结束开流，结束时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())):
            # 开流失败判定条件及处理：
            # ①开流40秒后如果播放器上的控件状态为不可用，即，视频质量切换、录像、截屏、静音的enabled is false；
            # ②或者开流40秒后如果app崩溃了，找不到播放器上的控件都视为开流失败；
            # ③截取app日志最新1000行、截取ty日志最新1000行，添加到allure的附件当中；
            if master.find_element(AppiumBy.ID,
                                   "com.glazero.android:id/btn_in_video_clarity_hd").is_enabled() is False and \
                    master.find_element(AppiumBy.ID,
                                        "com.glazero.android:id/btn_record_start").is_enabled() is False and \
                    master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_snapshot").is_enabled() is False and \
                    master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_unmute").is_enabled() is False:

                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)
                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 进入这个条件分支说明开流失败了
                # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                # 因为获取日志比较重要，所以截图放在获取日志的后面
                # 开流结束时 截一张图：
                close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close flow",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 将这个步骤的状态置为fail，该用例执行结果是：失败
                assert True is False

            elif gz_public.isElementPresent(driver=master, by="id",
                                            value="com.glazero.android:id/btn_in_video_clarity_hd") is False and \
                    gz_public.isElementPresent(driver=master, by="id",
                                               value="com.glazero.android:id/btn_record_start") is False:

                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)
                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 进入这个条件分支说明开流失败了
                # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                # 因为获取日志比较重要，所以截图放在获取日志的后面
                # 开流结束时 截一张图：
                close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close flow",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 将这个step置为fail，用例执行结果为失败
                assert True is False

            # 开流成功，走到这里
            # 开流结束时 截一张图：
            close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close flow",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

    @allure.title('V8P 长时间开流')
    @allure.story('用户使用V8P长时间开流')
    def test_v8p_open_flow_long_time(self, dev_name=gz_public.get_device_name(model='V8P')):
        """
        :前提条件：① 账号下要绑定V8P设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :处理流程：在开流过程中任何时候都可能失败，所以要定时检查当前开流状态，
        :例如，开流时长1小时，每5分钟检查一次，检查内容包括：①检查控件状态 ②如果失败则获取日志，并停止本次开流 ③截图
        """
        # 获取v8p设备的名字
        print("找到的设备名称是：", dev_name)

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，v8p'):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2: 点击前面拿到的设备名称，例如，可视门铃Pro'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step3: 进入指定设备的开流页面后开流60分钟，开始时间点为：%s' %
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            # 实时视频加载中… 等待3秒
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/tv_live_play_loading") is True:
                time.sleep(3)

            # 开流开始后 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/start_flow_%s.png" % start_flow, name="start_flow_%s" % start_flow,
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 开流时长设置为：12*300 = 3600秒
            for ii in range(1, 13):
                print("当前是第%s次" % ii)
                # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
                # 排除在开流阶段的网络波动导致开流中断的情况，如果在结束时仍为：刷新重试，那么认为开流失败
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/bt_play_retry") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/bt_play_retry').click()
                    master.implicitly_wait(10)

                # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/liveplay_power_prompt_got_it').click()
                    master.implicitly_wait(10)

                # 每5分钟检查一次，每次执行时间大概是20秒，15次一共是300秒
                for jj in range(1, 16):
                    print("当前是第 %s 次中的第 %s 次" % (ii, jj))
                    # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
                    # 排除在开流阶段的网络波动导致开流中断的情况，如果在结束时仍为：刷新重试，那么认为开流失败
                    if gz_public.isElementPresent(driver=master, by="id",
                                                  value="com.glazero.android:id/bt_play_retry") is True:
                        master.find_element(AppiumBy.ID, 'com.glazero.android:id/bt_play_retry').click()
                        master.implicitly_wait(10)

                    # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                    if gz_public.isElementPresent(driver=master, by="id",
                                                  value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                        master.find_element(AppiumBy.ID, 'com.glazero.android:id/liveplay_power_prompt_got_it').click()
                        master.implicitly_wait(10)
                    time.sleep(1)

                # 检查内容包括：①检查控件状态 ②如果失败则获取日志，并停止本次开流 ③截图
                # 开流失败判定条件及处理：
                # ①5分钟后如果播放器上的控件状态为不可用，即，视频质量切换、录像、截屏、静音的enabled is false；
                # ②或者开流5分钟后如果app崩溃了，找不到播放器上的控件都视为开流失败；
                # ③截取app日志最新1000行、截取ty日志最新1000行，添加到allure的附件当中；
                if master.find_element(AppiumBy.ID,
                                       "com.glazero.android:id/btn_in_video_clarity_hd").is_enabled() is False and \
                        master.find_element(AppiumBy.ID,
                                            "com.glazero.android:id/btn_record_start").is_enabled() is False and \
                        master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_snapshot").is_enabled() is False:

                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 进入这个条件分支说明开流失败了
                    # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                    # 因为获取日志比较重要，所以截图放在获取日志的后面
                    # 开流结束时 截一张图：
                    close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                    time.sleep(3)

                    # 将截图添加到报告中
                    allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close_flow_%s" % close_flow,
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)

                    # 将这个步骤的状态置为fail，该用例执行结果是：失败
                    assert True is False

                elif gz_public.isElementPresent(driver=master, by="id",
                                                value="com.glazero.android:id/btn_in_video_clarity_hd") is False and \
                        gz_public.isElementPresent(driver=master, by="id",
                                                   value="com.glazero.android:id/btn_record_start") is False:

                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 进入这个条件分支说明开流失败了
                    # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                    # 因为获取日志比较重要，所以截图放在获取日志的后面
                    # 开流结束时 截一张图：
                    close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                    time.sleep(3)

                    # 将截图添加到报告中
                    allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close_flow_%s" % close_flow,
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)

                    # 将这个step置为fail，用例执行结果为失败
                    assert True is False

                # 每次检查开流状态，都截一张图，如果长时间开流成功，一共会截12张图：
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="第 %s 次检查开流状态_开流状态正常_%s" % (ii, current_time),
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

        with allure.step('step4：点击页面左上角的 返回，结束开流，结束时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())):

            # 关闭开流时 截一张图：
            close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow, name="close_flow_%s" % close_flow,
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 确认回到了首页
            assert gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/img_tab_device") is True

    @allure.title('V8P 开流30分钟后自动断流')
    @allure.story('用户使用V8P开流30分钟后自动断流')
    def test_v8p_disconnect_flow_after_30_minutes(self, dev_name=gz_public.get_device_name(model='V8P')):
        """
        :前提条件：① 账号下要绑定V8P设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击；③如果中间有升级弹窗出现，脚本做兼容处理，点击取消或忽略本次升级，其他弹窗类似
        :设备要求：① 设备为在线状态，可以开流；② 网络稳定，可以考虑放在屏蔽箱里执行；③ 电量充足，不能关机
        :测试点：开流30分钟后会自动断流。APP表现为，开流到30分钟时播放器中状态为：实时视频加载中...持续15秒，15秒之后播放器中显示：视频打开失败，请重试+刷新重试，为最终断流结果
        :处理流程：
        ① 在开流开始时播放器的状态是：正在建立访问通道...   正在连接网络服务...
        ② 在开流过程中任何时候都可能失败，所以要定时检查当前开流状态；
        ③ 例如，开流时长30分钟，前25分钟，每5分钟检查一次，检查内容包括：
        （1）检查播放器控件状态和播放器当前的状态提示；
        （2）如果控件状态不可用或者在播放器上出现指定状态（参考 测试点中的状态），则视为本次开流失败；
        （3）获取app和ty日志，结束本次开流；
        （4）截图；
        ④最后5分钟等待断流标识出现，播放器中会出现：实时视频加载中...持续15秒，15秒之后播放器中显示：视频打开失败，请重试+刷新重试，为最终断流结果，截图；
        ⑤最后5分钟没有断流标识出现，获取app和ty日志，截图。
        """
        # 获取v8p设备的名字
        print("找到的设备名称是：", dev_name)

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，v8p'):
            # 确认找到了设备
            try:
                master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
                master.implicitly_wait(10)
            except NoSuchElementException:
                # 截图
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="没有找到设备_%s_%s" % (dev_name, current_time),
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                assert True is False, "没有找到给定的设备"
            else:
                pass

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2：点击前面拿到的设备名称，例如，可视门铃Pro'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step3: 开流开始后，前25分钟，每5分钟检查一次开流状态'):
            # 等待状态包括：正在建立访问通道...   正在连接网络服务...   实时视频加载中...   这些状态的id相同，如下：
            # 这些状态消失后，才成功开流
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/tv_live_play_loading") is True:
                time.sleep(1)

            # 成功开流后记录开始的时间戳
            connect_flow_ts = int(round(time.time() * 1000))
            print("开始开流时间是：", connect_flow_ts)

            # 开流开始后 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/V8P/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/V8P/start_flow_%s.png" % start_flow, name="start_flow_%s" % start_flow,
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 前25分钟每5分钟检查一次开流状态，5*300 = 1500秒，即25分钟
            for ii in range(1, 6):
                print("当前是第%s次" % ii)
                # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
                # 排除在开流阶段的网络波动导致开流中断的情况，如果在结束时仍为：刷新重试，那么认为开流失败
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/bt_play_retry") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/bt_play_retry').click()
                    master.implicitly_wait(10)

                # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                if gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                    master.find_element(AppiumBy.ID, 'com.glazero.android:id/liveplay_power_prompt_got_it').click()
                    master.implicitly_wait(10)

                # 每5分钟检查一次，每次执行时间大概是19秒，16次一共是304秒即5分钟
                for jj in range(1, 17):
                    print("当前是第 %s 次中的第 %s 次" % (ii, jj))
                    # 如果出现：当前网络不可用，请检查网络连接，点击：刷新重试
                    # 排除在开流阶段的网络波动导致开流中断的情况，如果在结束时仍为：刷新重试，那么认为开流失败
                    # 20230531：强校验，如果出现刷新重试，那么认为开流失败
                    # if gz_public.isElementPresent(driver=master, by="id",
                    #                               value="com.glazero.android:id/bt_play_retry") is True:
                    #     master.find_element_by_id('com.glazero.android:id/bt_play_retry').click()
                    #     master.implicitly_wait(10)

                    # 如果出现：长时间查看实时视频会加速门铃电量消耗，是否为您退出实时视频？，点击：继续观看
                    if gz_public.isElementPresent(driver=master, by="id",
                                                  value="com.glazero.android:id/liveplay_power_prompt_got_it") is True:
                        master.find_element(AppiumBy.ID, 'com.glazero.android:id/liveplay_power_prompt_got_it').click()
                        master.implicitly_wait(10)
                    time.sleep(9)

                # 检查内容包括：①检查控件状态 ②如果失败则获取日志，并停止本次开流 ③截图
                # 开流失败判定条件及处理：
                # ①5分钟后如果播放器上的控件状态为不可用，即，视频质量切换、录像、截屏、静音的enabled is false；
                # ②或者开流5分钟后如果app崩溃了，找不到播放器上的控件都视为开流失败；
                # ③截取app日志最新1000行、截取ty日志最新4000行，添加到allure的附件当中；
                if master.find_element(AppiumBy.ID,
                                       "com.glazero.android:id/btn_in_video_clarity_hd").is_enabled() is False and \
                        master.find_element(AppiumBy.ID,
                                            "com.glazero.android:id/btn_record_start").is_enabled() is False and \
                        master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_snapshot").is_enabled() is False:

                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 进入这个条件分支说明开流失败了
                    # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                    # 因为获取日志比较重要，所以截图放在获取日志的后面
                    # 开流结束时 截一张图：
                    close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                    time.sleep(3)

                    # 将截图添加到报告中
                    allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow,
                                       name="开流失败_播放器控件的enable属性是false_%s" % close_flow,
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)

                    # 将这个步骤的状态置为fail，该用例执行结果是：失败
                    assert True is False, "检查开流状态，播放器中的控件 enable属性is false，开流失败"

                elif gz_public.isElementPresent(driver=master, by="id",
                                                value="com.glazero.android:id/btn_in_video_clarity_hd") is False and \
                        gz_public.isElementPresent(driver=master, by="id",
                                                   value="com.glazero.android:id/btn_record_start") is False:

                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 进入这个条件分支说明开流失败了
                    # 断言失败后就不执行后面的步骤了，所以在这里截一张图
                    # 因为获取日志比较重要，所以截图放在获取日志的后面
                    # 开流结束时 截一张图：
                    close_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    master.save_screenshot('./report/V8P/close_flow_%s.png' % close_flow)
                    time.sleep(3)

                    # 将截图添加到报告中
                    allure.attach.file("./report/V8P/close_flow_%s.png" % close_flow,
                                       name="开流失败_没有找到播放器中的控件_%s" % close_flow,
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)

                    # 将这个step置为fail，用例执行结果为失败
                    assert True is False, "没有找到播放器中的控件，可能是app崩溃，或者崩到其他页面，开流失败"

                # 每次检查开流状态，都截一张图，如果长时间开流成功，一共会截5张图：
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="第 %s 次检查开流状态_开流状态正常_%s" % (ii, current_time),
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

        with allure.step(
                'step4：后5分钟，等待出现断流标识，播放器中出现”实时视频加载中...“，15秒后出现，视频打开失败，请重试+刷新重试'):
            # 等待断流的标志出现，即播放器中出现：实时视频加载中...持续15秒
            try:
                WebDriverWait(master, timeout=310, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.ID,
                                             "com.glazero.android:id/tv_live_play_loading").text == '实时视频加载中…')
            except TimeoutException:
                # 没有找到标识行的元素会抛出异常，获取app和ty日志，并截一张图，如果不放在except中，会直接结束程序不能执行后面的语句：
                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/V8P/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/V8P/log_attch', 4000)

                # 将日志添加到报告中
                allure.attach.file("./report/V8P/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 截图
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="没有找到 ”实时视频加载中...“ 的元素_%s" % current_time,
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 用例状态置为fail，结束用例
                assert True is False, "没有出现断流标识，播放器中没有出现”实时视频加载中...，30分钟后没有自动断流"
            else:
                # 断流时获取当前时间戳
                disconnect_flow_ts = int(round(time.time() * 1000))
                print('断流时间是：', disconnect_flow_ts)

                # 等待的元素出现了，实时视频加载中...的元素已经找到，截一张图：
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="”实时视频加载中...“ 的元素出现了_ok_%s" % current_time,
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

            # 15秒之后播放器中显示：视频打开失败，请重试+刷新重试，为最终断流结果
            try:
                WebDriverWait(master, timeout=20, poll_frequency=2).until(
                    lambda x: x.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="视频打开失败，请重试"]'))
            except TimeoutException:
                # 没有找到标识行的元素会抛出异常，截一张图，如果不放在except中，会直接结束程序不能执行后面的语句：
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="没有找到 ”视频打开失败，请重试+刷新重试“ 的元素_%s" % current_time,
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

                # 用例状态置为fail，结束用例
                assert True is False, "播放器中没有出现：视频打开失败，请重试+刷新重试"
            else:
                # 等待的元素出现了，视频打开失败，请重试+刷新重试的元素已经找到，截一张图：
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/V8P/check_flow_status_%s.png' % current_time)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/V8P/check_flow_status_%s.png" % current_time,
                                   name="”视频打开失败，请重试+刷新重试“ 的元素出现了_ok_%s" % current_time,
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)

        with allure.step('step5：校验断流的时间点距离开流的时间点间隔是30分钟即1800秒'):
            with allure.step('step5-1：开流时间点为：%s' % connect_flow_ts):
                pass
            with allure.step('step5-2：断流时间点为：%s' % disconnect_flow_ts):
                pass
                # 在step3和step4中已经获得了 开流时间点和断流时间点，计算差值
                result = int(disconnect_flow_ts - connect_flow_ts)
                print("断流时间点和开流时间点差值是：", result)
                res_sec = result // 1000
                print("开流时长是：%d秒" % res_sec)
            with allure.step('step5-3：断流时间点和开流时间点差值是：%d秒' % res_sec):
                # 断言误差在10秒之内，程序运行时间，例如，截图、保存、allure处理附件等，实际看误差有：1秒，2秒、3秒
                assert (res_sec - 1800) <= 10, "实际开流时间大于1810秒"

        with allure.step('step6：点击页面左上角的 返回，结束开流，结束时间点为：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())):
            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 确认回到了首页
            assert gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/img_tab_device") is True

    @allure.title('C6L 多次开流')
    @allure.story('用户循环测试C6L的开流-关流，即多次开流')
    def test_c6l_open_flow(self, dev_name=gz_public.get_device_name(model='C6L')):
        """
        :前提条件：① 账号下要绑定C6L设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        # 获取c6l设备的名字
        print("找到的设备名称是：", dev_name)

        with allure.step(
                'step1: 等待25秒，设备休眠。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 在屏蔽箱里从退出开流到休眠18秒
            time.sleep(25)

        with allure.step('step2: 在设备列表中滑动找到要开流的设备，例如，c6l。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，c6l。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 判断开流结果，加载过程消失后开流成功或者失败
            play_state = initPhone.get_dev_play_state("C6L2BA110005310")
            print("当前开流状态是：%s" % play_state)

            # 开流失败时处理
            if play_state == 'playState:Playing':
                assert play_state == 'playState:Playing', "playState是Playing 开流成功。"
            else:
                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/C6L/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/C6L/log_attch/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/C6L/log_attch', 4000)
                # 将日志添加到报告中
                allure.attach.file("./report/C6L/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                assert play_state == 'playState:Playing', "playState不是Playing 开流失败。"

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

    def test_public_open_flow(self, dev_model):
        """
        :前提条件：① 账号下要绑定准备开流的设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        dev_name = gz_public.get_device_name(model=dev_model)
        # 获取设备的名字
        print("找到的设备名称是：%s，设备型号是：%s" % (dev_name, dev_model))

        with allure.step(
                'step1: 等待25秒，设备休眠。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 在屏蔽箱里从退出开流到休眠18秒
            time.sleep(25)

        with allure.step('step2: 在设备列表中滑动找到要开流的设备，例如，%s。step时间点：%s'
                         % (dev_model, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

        with allure.step('step3: 点击前面拿到的设备名称，例如，%s。step时间点：%s'
                         % (dev_model, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/C6L_C9L/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/C6L_C9L/start_flow_%s.png" % start_flow, name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 判断开流结果，加载过程消失后开流成功或者失败
            play_state = initPhone.get_dev_play_state()
            print("当前开流状态是：%s" % play_state)

            if play_state == 'playState:Playing':
                assert play_state == 'playState:Playing', "playState是Playing 开流成功。"
            # 开流失败时处理
            else:
                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/C6L_C9L/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/C6L_C9L/log_attach/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/C6L_C9L/log_attch', 4000)
                # 将日志添加到报告中
                allure.attach.file("./report/C6L_C9L/log_attach/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # assert play_state == 'playState:Playing', "playState不是Playing 开流失败。"
                # 软断言，失败后可以继续执行
                pytest.assume(play_state == 'playState:Playing')
                self.fail_flag = 1

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            master.implicitly_wait(10)

            # 智能提醒弹窗button，知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/button") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 低电量提醒弹窗，知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_dialog_confirm") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 确认回到了首页
            assert gz_public.isElementPresent(driver=master, by="id",
                                              value="com.glazero.android:id/img_tab_device") is True

    @allure.title('C6L、C9L 多次开流')
    @allure.story('用户循环测试C6L、C9L的开流-关流，即多次开流')
    def test_c6l_c9l_open_flow(self):
        """
        :前提条件：① 账号下要绑定C6L、C9L设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        with allure.step('step1: C6L开流。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            self.test_public_open_flow('C6L')
            c6l_fail_flag = self.fail_flag
            self.fail_flag = 0

        with allure.step('step2: C9L开流。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            self.test_public_open_flow('C9L')
            c9l_fail_flag = self.fail_flag

        if c6l_fail_flag == 0 and c9l_fail_flag == 0:
            with allure.step('step3: 判断C6L、C9L开流是否成功：C6L、C9L 都开流成功。'):
                assert (c6l_fail_flag == 0 and c9l_fail_flag == 0), "C6L、C9L 都开流成功。"
        elif c6l_fail_flag == 1 and c9l_fail_flag == 1:
            with allure.step('step3: 判断C6L、C9L开流是否成功：C6L、C9L 开流都失败。'):
                assert (c6l_fail_flag == 0 and c9l_fail_flag == 0), "C6L、C9L 开流都失败。"
        elif c6l_fail_flag == 0 and c9l_fail_flag == 1:
            with allure.step('step3: 判断C6L、C9L开流是否成功：C6L开流成功、C9L开流失败。'):
                assert (c6l_fail_flag == 0 and c9l_fail_flag == 0), "C6L开流成功、C9L开流失败。"
        elif c6l_fail_flag == 1 and c9l_fail_flag == 0:
            with allure.step('step3: 判断C6L、C9L开流是否成功：C6L开流失败、C9L开流成功。'):
                assert (c6l_fail_flag == 0 and c9l_fail_flag == 0), "C6L开流失败、C9L开流成功。"

        with allure.step('step4: 冷启app。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

    @allure.title('C9S 多次开流 ')
    @allure.story('用户循环测试C9S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c9s_open_flow(self, dev_name=gz_public.get_device_name(model='C9S')):
        """
        :前提条件：① 账号下要绑定C9S设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
        :设备为在线状态，可以开流
        :网络稳定，可以考虑放在屏蔽箱里执行
        :电量充足，不能关机
        :如果中间有升级弹窗出现，点击取消或忽略本次升级，其他弹窗类似
        :步骤：
        :1. 确认设备已休眠
        :2. 冷启动App
        :3. 开流，等结果（成功 or 失败）
        :重复以上 1 2 3，记录下每次的结果
        """
        # 获取c9s设备的名字
        print("找到的设备名称是：", dev_name)

        with allure.step(
                'step1: 等待25秒，设备休眠。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 在屏蔽箱里从退出开流到休眠18秒
            time.sleep(25)

        with allure.step('step2: 在设备列表中滑动找到要开流的设备，例如，c9s。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，c9s。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_name).click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            # 进入首页后检查，是否有低电量提醒弹窗-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_live_play_guide_next") is True:
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 变声对讲引导 ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航 ,点击屏幕中的 下一波
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '下一步').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第二个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)
                # 首次安装 APP 进入开流页面,屏幕出现引导动画 -- 一键巡航第三个引导页面  ,点击屏幕中的 知道了
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '知道了').click()
                master.implicitly_wait(10)

            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)
            '''
            # 当开流不成功,屏幕出现刷新重试时,点击刷新重试按钮.
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/bt_play_retry") is True:
                master.implicitly_wait(10)
                # 点击屏幕刷新重试按钮.
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '刷新重试').click()
                time.sleep(40)

                # 截一张图
                start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
                time.sleep(3)

                # 将截图添加到报告中
                allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
                                   attachment_type=allure.attachment_type.JPG)
                master.implicitly_wait(10)
            '''
            with allure.step('step4-1: 查看从首页，进入开流页面的结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,进入开流页面的状态，日志中出现字符串 LivePlayFragment:onCreate 表示设备唤醒成功。
                create_LivePlay_fragment_state = initPhone.get_start_create_LivePlay_fragment_result(
                    initPhone.get_dev_id(), click_time)
                print("开流播放片段 创建成功：%s" % create_LivePlay_fragment_state)

                # 进入开流页面失败时处理
                if create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate':
                    assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备创建开流页面成功。"
                else:
                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志,并且保存到本地
                    gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备唤醒成功。"

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 和  wakeSuccess 表示设备唤醒成功。
                start_wake_state = initPhone.get_dev_start_wake_state_result(initPhone.get_dev_id(), click_time)
                print("设备收到开始唤醒指令的状态是：%s" % start_wake_state)

                # 设备唤醒失败时处理
                if start_wake_state == 'wakeStart':
                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备成功 收到开始唤醒指令。"
                else:
                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志,并且保存到本地
                    gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备成功 收到开始唤醒指令。"

            with allure.step('step4-3: 进入开流页面，查看设备唤醒结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
                dev_wake_state = initPhone.get_dev_wake_state_result(initPhone.get_dev_id(), click_time)
                print("当前设备唤醒状态是：%s" % dev_wake_state)

                # 设备唤醒失败时处理
                if dev_wake_state == 'wakeSuccess':
                    assert dev_wake_state == 'wakeSuccess', "wakeSuccess 表示设备唤醒成功。"
                else:
                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志,并且保存到本地
                    gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert dev_wake_state == 'wakeSuccess', "wakeSuccess 表示设备唤醒成功。"

            with allure.step('step4-4: 进入开流页面，查看P2P连接结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
                dev_p2p_state = initPhone.get_dev_p2p_state_result(initPhone.get_dev_id(), click_time)
                print("当前设备P2P状态是：%s" % dev_p2p_state)

                # 设备唤醒失败时处理
                if dev_p2p_state == 'success':
                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"
                else:
                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"

            with allure.step('step4-5: 进入开流页面，查看开流结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流结果，加载过程消失后开流成功或者失败
                play_state = initPhone.get_dev_play_state_result(initPhone.get_dev_id(), click_time)
                print("当前开流状态是：%s" % play_state)

                # 开流失败时处理
                if play_state == 'state:Playing':
                    assert play_state == 'state:Playing', "state是Playing 开流成功。"
                else:
                    # 在手机中查找对应的日志文件
                    current_date = time.strftime("%Y%m%d", time.localtime())

                    # 获取当前时间，用于区分不同的日志文件作为附件。
                    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                    # 获取app日志
                    gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    # 获取ty日志
                    gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                    # 将日志添加到报告中
                    allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                       attachment_type=allure.attachment_type.TEXT)
                    master.implicitly_wait(10)

                    with allure.step('step4-3-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert play_state == 'state:Playing', "state是Playing 开流成功。"

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            time.sleep(40)

            # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
            dev_dormancy_state = initPhone.get_dev_dormancy_state_result(initPhone.get_dev_id(),
                                                                         click_time)
            print("当前设备休眠状态是：%s" % dev_dormancy_state)

            # 设备唤醒失败时处理
            if dev_dormancy_state == 'dpStr={"149":false}':
                assert dev_dormancy_state == 'dpStr={"149":false}', "'dpStr={\"149\":false}' 表示设备休眠成功。"
            else:
                # 在手机中查找对应的日志文件
                current_date = time.strftime("%Y%m%d", time.localtime())

                # 获取当前时间，用于区分不同的日志文件作为附件。
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

                # 获取app日志
                gz_public.get_app_log('app', current_date, current_time, './report/C9S/log_attch', 1000)

                # 将日志添加到报告中
                allure.attach.file("./report/C9S/log_attch/app_log_%s.log" % current_time, name="app log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                # 获取ty日志
                gz_public.get_app_log('ty', current_date, current_time, './report/C9S/log_attch', 4000)
                # 将日志添加到报告中
                allure.attach.file("./report/C9S/log_attch/ty_log_%s.log" % current_time, name="ty log",
                                   attachment_type=allure.attachment_type.TEXT)
                master.implicitly_wait(10)

                with allure.step('step5-1-1: 冷启app。step时间点：%s'
                                 % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                    # appium 1.22.2的用方法
                    # master.close_app()
                    master.terminate_app(android_package_name)
                    master.implicitly_wait(10)

                # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                assert dev_dormancy_state == 'dpStr={"149":false}', "dpStr={\"149\":false} 表示设备休眠成功。"

                # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)


if __name__ == '__main__':
    # pytest.main(["-q", "-s", "-ra", "test_gzAndroidAuto.py::TestUserCenter::test_logOut"])

    # C6SP 绑定
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestAddDevices::test_addC6SP_station",
    #             "--alluredir=./report/C6SP"])

    # C2E 绑定
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestAddDevices::test_addC2E",
    #              "--alluredir=./report/C2E"])

    # C2E 校准
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1000, "test_gzAndroidAuto.py::TestDeviceList::test_C2E_Calibrate",
    #             "--alluredir=./report/C2E"])

    # V8P 多次开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 3, "test_gzAndroidAuto.py::TestOpenFlow::test_v8p_open_flow",
    #              "--alluredir=./report/V8S"])

    # V8P 长时间开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 20, "test_gzAndroidAuto.py::TestOpenFlow"
    #                                                    "::test_v8p_disconnect_flow_after_30_minutes",
    #              "--alluredir=./report/V8P"])

    # C6L 多次开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestOpenFlow::test_c6l_open_flow",
    #              "--alluredir=./report/C6L"])

    # C6L、C9L 多次开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 2, "test_gzAndroidAuto.py::TestOpenFlow::test_c6l_c9l_open_flow",
    #              "--alluredir=./report/C6L_C9L"])

    # C9S 多次开流
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_gzAndroidAuto.py::TestOpenFlow::test_c9s_open_flow",
                 "--alluredir=./report/C9S"])
