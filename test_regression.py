"""
----------------------------------
@Author: Zhang jia min
@Version: 1.0
@Date: 20230517
@desc: 回归用例
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
import os

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['Galaxy S10e', 'moto g', 'SamsungA51', 'moto_z4']

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

    # StartAppium.start_appium(port=phone_1["port"])
    time.sleep(3)
    # master = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_1["port"], phone_1["des"])
    print('port: ', phone_1['port'])
    print('des:', phone_1['des'])
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
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)

    @allure.story('用户名和密码输入框右侧的关闭按钮和显示/隐藏按钮')
    def test_gzLoginClearShowHide(self):
        with allure.step('step1: 在splash页，点击 登录 按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

            # 断言进入了登录页面
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title_string").text == "登录"

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

        with allure.step('step7: 返回到splash页面'):
            # 点击 右上角的关闭按钮
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_title_close").click()
            master.implicitly_wait(10)

            # 回到 splash页面，断言登录和创建账号按钮（不断言文本，因为跟语言变化）
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login")
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_create_account")

    @allure.story('输入用户名和密码登录aosu app')
    def test_gzLogin(self, user_name=gz_public.email, pass_word=gz_public.pwd, region=gz_public.REGION):
        # 点击 aosu 图标7次，在地区列表中出现中国
        x = master.get_window_size()['width']
        y = master.get_window_size()['height']
        xx = x//2
        yy = y//2
        for ii in range(1, 8):
            # master.find_elements_by_class_name("android.widget.ImageView")[0].click()
            # appium2.0.1找不到该元素
            # master.find_element(AppiumBy.CLASS_NAME, "android.widget.ImageView").click()
            # 点击屏幕中间7次
            master.tap([(xx, yy)], 500)
            master.implicitly_wait(1)

        with allure.step('step1：在splash页，点击 登录 按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/splash_login").click()
            master.implicitly_wait(10)

            # 断言进入了登录页面
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == "登录"

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
            '''
            # 如果默认是指定的地区，那么就直接点击登录
            if master.find_elements_by_id("com.glazero.android:id/edit_text")[2].text[-3:] == region:
                time.sleep(1)
            else:
                # 如果默认不是指定的地区，那么就在地区列表中选择
            '''
            # 在回归用例中不能直接点击登录按钮，要走一遍地区选择过程
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/edit_text")[2].click()
            master.implicitly_wait(10)
            # master.find_element_by_android_uiautomator( 'new UiScrollable(new UiSelector().scrollable(
            # true)).scrollIntoView(new UiSelector().text("%s"))' % region)
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector('
                                ').text("%s"))' % region)
            master.implicitly_wait(10)
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % region).click()  # 此时只能写类名
            master.implicitly_wait(10)
            time.sleep(1)

        with allure.step('step5：点击 登录 按钮'):
            # 点击登录按钮之前截图
            ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/regression/login_%s.png' % ts)
            time.sleep(3)

            allure.attach.file("./report/regression/login_%s.png" % ts, name="登录页面",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
            master.implicitly_wait(10)

        with allure.step('step6: 登录成功'):
            # 点击登录按钮之后即进入首页后截图截图
            time.sleep(5)
            master.save_screenshot('./report/regression/homePage.png')
            time.sleep(3)

            allure.attach.file("./report/regression/homePage.png", name="登陆成功 进入首页",
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 登录后进入首页，有可能会弹出低电量的弹窗，发现后点击“知道了”关闭弹窗
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_dialog_confirm") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_dialog_confirm").click()
                master.implicitly_wait(10)

            # 出现固件升级弹窗后，点击 取消/忽略此版本，多个弹窗的话，点击多次
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/inner_layout_ota_prompt") is True:
                master.find_elements(AppiumBy.ID, "com.glazero.android:id/button")[1].click()
                master.implicitly_wait(10)

            # 如果出现智能提醒，点击：知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_iv_top_icon") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/button").click()
                master.implicitly_wait(10)

            # 如果出现了新人礼的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/img_ad") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
                master.implicitly_wait(10)

            """
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/inner_layout_ota_prompt") is True:
                master.find_element_by_xpath('//android.widget.Button[@text="忽略此版本"]').click()
                master.implicitly_wait(10)
            """
            time.sleep(3)

            # 没有设备的情况下启动app后会进入select model页面，兼容该页面，点击返回<，回到首页
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/tv_title_string") is True:
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
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_playback")
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_service")


'''
    @staticmethod
    def teardown_method():
        master.close_app()
        master.implicitly_wait(10)
'''


@allure.feature('用户中心模块')
class TestUserCenter(object):
    # 执行这个测试类，前提条件是要登录，登录后才能执行这组用例
    # 登录前先要启动app
    # 那么就要使用setup_class
    @staticmethod
    def setup_class():
        """
        master.close_app()
        master.implicitly_wait(10)
        master.launch_app()
        master.implicitly_wait(10)
        """
        # 如果单独执行某一条用例那么需要放开这段代码，如果整体执行，需要注释掉这段代码：
        # 如果app没有启动，那么启动app
        if master.current_activity != ".SplashActivity":
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)

        # 登录状态下启动app 进入首页 activity 是：.SplashActivity，不是：.account.login.LoginActivity，所以不能通过activity判断是否在首页
        # 通过登录后首页左上角的menu图标判断
        if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_menu") is False:
            TestGzLogin.test_gzLogin(self=NotImplemented)
            master.implicitly_wait(10)

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

    @allure.story('修改登录密码')
    def test_changePassword(self, old_pass_word=gz_public.pwd, new_pass_word='Qwe101010'):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 账号管理'):
            # 使用下标的时候第一个元素容易点错
            # master.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[0].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="账号管理"]').click()  # 此时只能写类名
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

    @allure.story('设备分享')
    def test_device_share(self):
        with allure.step('step1：点击用户中心菜单'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_menu').click()
            master.implicitly_wait(10)

        with allure.step('step2：点击 设备分享 项'):
            # master.find_elements_by_id('com.glazero.android:id/tv_menu_item_name')[1].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="设备分享"]').click()
            master.implicitly_wait(10)

            # 当出现 Aosu 蓝牙和附近的设备权限 弹窗时,点击允许
            while gz_public.isElementPresent(driver=master, by="xpath",
                                             value='//android.widget.TextView[@text="“Aosu”想要使用蓝牙和附近的设备权限"]') is True:
                # 点击 允许按钮
                master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="允许"]').click()
                master.implicitly_wait(10)
                break

            # 当出现 Aosu 附近的设备权限 弹窗时,点击允许
            while gz_public.isElementPresent(driver=master, by="xpath",
                                             value='//android.widget.TextView[@text="要允许“Aosu”查找、连接到附近设备以及确定附近设备的相对位置吗？"]') is True:
                # 点击 允许按钮
                master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="允许"]').click()
                master.implicitly_wait(10)
                break

            # 当出现 打开系统蓝牙 弹窗时,点击 X 按钮
            while gz_public.isElementPresent(driver=master, by="xpath",
                                             value='//android.widget.TextView[@text="打开系统蓝牙"]') is True:
                # 点击 X 按钮
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/iv_close').click()
                master.implicitly_wait(10)
                break

            # 当出现 打开系统蓝牙 动画弹窗时,点击 X 按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value='com.glazero.android:id/iv_close') is True:
                # 点击 X 按钮
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/iv_close').click()
                master.implicitly_wait(10)

                # 进入手机首页,打开通知栏。
                master.open_notifications()
                time.sleep(1)

                # 点击打开手机的 蓝牙 按钮
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="蓝牙"]').click()

                # 点击手机返回按钮,返回到 Aosu
                initPhone.keyEventSend(4)
                break

        # 前提账号下有设备
        with allure.step('step3：点击 邮箱分享'):
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="邮箱分享"]').click()
            master.implicitly_wait(10)

        with allure.step('step4：输入分享邮箱的地址,点击下一步'):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/edt_share_user_email').click()
            master.implicitly_wait(10)
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/edt_share_user_email').send_keys(
                gz_public.home_user)
            master.implicitly_wait(10)
            master.hide_keyboard()

            # 选中设备并填写邮箱后，页面底部按钮变成高亮可以点击
            assert master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="下一步"]').is_enabled() is True

            # 点击 下一步 按钮
            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="下一步"]').click()

        with allure.step('step5：选择设备,选择分享权限，例如第一个设备和第二个设备'):
            # 注意:因为进入到选择设备页面,第一个设备已经默认选中,所以 只需要再选择  分享权限  即可
            # 查看 默认选中的第一个设备,是否已经分享,当前账号下设备是否还有 可分享的设备

            # 管理员权限
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="管理员"]').click()
            # 普通成员权限
            # master.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="普通成员"]').click()

        with allure.step('step6：点击 分享设备 按钮'):
            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="分享设备"]').click()
            master.implicitly_wait(20)

            # toast = WebDriverWait(driver=master, timeout=45, poll_frequency=2).until(
            #     lambda x: x.find_element(AppiumBy.XPATH, '//*[text="邀请已发送"]'))
            get_toast_text = gz_public.get_toast_text(master, "邀请已发送")

            # 如果 获取到的 toast 是 邀请已发送,即 分享成功
            assert get_toast_text == '邀请已发送'

            # if gz_public.isElementPresent(driver=master, by="id", value="com.glazero.android:id/img_prompt_image"):
            #     master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_share_management').click()
            #     master.implicitly_wait(10)

        with allure.step('step7：验证:进入 分享管理 查看 我分享的中 是否分享成功'):

            with allure.step('step7-1：点击 分享管理 按钮'):
                # 点击 分享管理 按钮
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/iv_right').click()

            with allure.step('step7-2：点击 分享管理页面 我分享的 中第1个用户 '):
                # 点击 点击 分享管理页面 我分享的 中第1个用户
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/iv_next').click()

            with allure.step('step7-3：验证：邮箱是分享时填写的邮箱 且 已分享的设备按钮 处于浅蓝色开启状态 '):

                #  获取到的 被分享的家人 邮箱
                get_shared_family_mail = master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_email').text
                #  获取到的 被分享的设备按钮 状态
                get_shared_family_device = master.find_element(AppiumBy.ID, 'com.glazero.android:id/iv_switch').text

                # 如果 分享管理页面获取到的  被分享的家人邮箱 与 分享时填写的家人邮箱一致,且 分享设备按钮未浅蓝色 开启 状态,即分享成功
                if get_shared_family_mail == gz_public.home_user and get_shared_family_device == '开启':
                    print("分享成功")
                else:
                    print("分享失败")

    @allure.story('云录')
    def test_cloud(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 云录 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[2].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="云录"]').click()
            master.implicitly_wait(10)

            time.sleep(3)

            # 如果是新用户，跳到介绍页面，断言右上角是云录入口，展示云存介绍页面，展示 立即开通 按钮
            if gz_public.get_user_type() == 1:
                assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_buy_cloud").is_enabled() is True
                # 20230809 ui调整
                # assert master.find_element(AppiumBy.ID,
                #                            "com.glazero.android:id/iv_cloud_equity_details_1").is_enabled() is True
                assert master.find_element(AppiumBy.XPATH,
                                           '//android.widget.TextView[@text="立即体验"]').is_enabled() is True

                with allure.step('step3: 点击 立即体验 按钮，进入云存商城页面'):  # 2024.03.28 该按钮文案由 立即领取 修改为  立即体验
                    master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="立即体验"]').click()
                    master.implicitly_wait(10)

                    time.sleep(3)

                    assert master.find_element(AppiumBy.ID, "com.glazero.android:id/hy_toolbar_title").text == '云存储'
                    assert master.find_element(AppiumBy.ID,
                                               "com.glazero.android:id/hy_sub_title").text == '更多'  # 2024.03.28 该按钮文案由 订单 修改为  更多

                with allure.step('step4: 返回到首页'):
                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    # 断言回到首页
                    assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")

            # 如果是老用户，跳到云存商城页面，断言标题为：云存储，右上角是：订单 按钮
            if gz_public.get_user_type() == 2:
                assert master.find_element(AppiumBy.ID, "com.glazero.android:id/hy_toolbar_title").text == '云存储'
                assert master.find_element(AppiumBy.ID,
                                           "com.glazero.android:id/hy_sub_title").text == '更多'  # 2024.03.28 该按钮文案由 订单 修改为  更多

                with allure.step('step3: 返回到首页'):
                    initPhone.keyEventSend(4)
                    time.sleep(1)

                    # 断言回到首页
                    assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu")

    @allure.story('常见问题列表')
    def test_frequent_question(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 常见问题列表 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[3].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="常见问题列表"]').click()
            master.implicitly_wait(10)

            # 校验loading页面
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/webview_loading")

            # 页面加载时间较慢
            time.sleep(5)

            # 页面加载完成后，校验页面的标题：常见问题列表
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '常见问题列表'

        with allure.step('step3: 点击下面的问题，例如，如何安装门铃？'):
            master.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='如何安装门铃？']").click()
            master.implicitly_wait(10)

            # 页面加载时间较慢
            time.sleep(5)

            # 校验页面内容正确
            assert master.find_element(AppiumBy.XPATH,
                                       "//android.widget.TextView[@text='为了确保设备安全，我们推荐您使用螺丝安装背板至墙壁上。']")

        with allure.step('step4: 点击左上角的返回按钮，回到前一页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

            # 页面加载时间较慢
            time.sleep(5)

        with allure.step('step5: 选择不同的设备，例如选择：电池版门铃 Pro'):
            # 使用控件id不能找到webview元素
            # master.find_element_by_id("tab_v8p").click()
            # 改换xpath
            master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='电池版门铃 Pro']").click()
            master.implicitly_wait(10)

            # 页面加载时间较慢
            time.sleep(5)

        with allure.step('step6: 点击下面的问题，例如，基站可以放置在离路由器多远的地方？'):
            master.find_element(AppiumBy.XPATH,
                                "//android.widget.Button[@text='基站可以放置在离路由器多远的地方？']").click()
            master.implicitly_wait(10)

            # 页面加载时间较慢
            time.sleep(5)
            assert_text = '理论上，基站可以距离路由器 12米/40 英尺以内。实际范围因许多因素变化而有所不同，例如墙壁的厚度、房屋内的障碍物以及路由器的位置。\n* ' \
                          '注意：请保持室内基站的天线与路由器的天线保持平行'
            # 校验页面内容正确
            assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='%s']" % assert_text)

        with allure.step('step7: 点击左上角的返回按钮，回到前一页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

            # 页面加载时间较慢
            time.sleep(5)

        with allure.step('step8: 点击左上角的返回按钮，退出 常见问题列表页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

    @allure.story('问题反馈')
    def test_feedback(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 问题反馈 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[4].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="问题反馈"]').click()
            master.implicitly_wait(10)

            # 页面加载完成后，校验页面的标题：问题反馈
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '问题反馈'

        with allure.step('step3: 选择设备，选择第一个设备'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/iv_device_stroke")[0].click()
            master.implicitly_wait(10)

        with allure.step('step4: 点击输入框，输入反馈内容'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/ed_feedback_content").clear()
            master.implicitly_wait(10)

            master.find_element(AppiumBy.ID, "com.glazero.android:id/ed_feedback_content").click()
            master.implicitly_wait(10)

            feedback_content = "李老師是我的第一個英語老師，她非常的漂亮和年輕，我們同學們都非常的喜歡她也喜歡聽她的英語課，我們都稱她為miss " \
                               "lee，因為這在英文中是對於老師的一種稱呼。\n" \
                               "李老師經常會在我們交上去的作業本上寫着一些讓我們覺得充滿希望的話語，她總是經常的在本子上寫一些鼓勵我們的話語，" \
                               "每次我們交作業的時候，我們都會非常的期待着李老師給我們的回復，這是我所期待的一件事情。"

            master.find_element(AppiumBy.ID, "com.glazero.android:id/ed_feedback_content").send_keys(feedback_content)
            master.implicitly_wait(10)

            master.hide_keyboard()

        with allure.step('step5: 上传图片'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/fl_take_photo").click()
            master.implicitly_wait(10)

            # 从相册中选择照片
            master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_album").click()
            master.implicitly_wait(10)

            # 场景兼容，Android 12 moto g 进入相册后显示分类文件夹
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.google.android.apps.photos:id/title") is True:
                master.find_element(AppiumBy.XPATH,
                                    '//android.widget.TextView[@text="相册"]').click()  # 2024.03.28 text由 照片 修改成 相册
                master.implicitly_wait(10)

                # 选择第一张照片
                # master.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")[0].click()
                # master.find_element(AppiumBy.ACCESSIBILITY_ID, '拍摄于*')
                # master.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("拍摄于")').click()
                master.tap([(0, 543), (264, 807)], 300)
                master.implicitly_wait(10)

                # 选取 顶部 第一张相册照片
                # master.find_element(AppiumBy.CLASS_NAME, 'android.widget.ImageView').click()

            # 场景兼容，Android 10 三星A51 进入相册后显示图片
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.sec.android.gallery3d:id/thumbnail") is True:
                # 选择第一张照片
                master.find_elements(AppiumBy.ID, "com.sec.android.gallery3d:id/thumbnail")[0].click()
                master.implicitly_wait(10)

        with allure.step('step6: 点击 发送 按钮'):
            # 需要滑动一下之后能找到 发送 按钮
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector('
                                ').text("发送"))')
            master.implicitly_wait(10)

            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="发送"]').click()  # 此时只能写类名

            # 校验等待状态
            WebDriverWait(master, timeout=60, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID,
                                         "com.glazero.android:id/pb_progress_bar"))  # 修改  知道loading 消失,执行下一步

            master.implicitly_wait(10)

            # 反馈成功后回到侧边栏页面（仅指Android端）
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon")

    @allure.story('联系我们')
    def test_contact_us(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 联系我们 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[5].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="联系我们"]').click()
            master.implicitly_wait(10)

            # 页面加载完成后，校验页面的标题：联系我们
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '联系我们'

        with allure.step('step3: 点击 美国电话'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/contact_number")[0].click()
            master.implicitly_wait(10)

            # 校验弹出拨打弹窗
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number")

        with allure.step('step4: 拨打电话'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number").click()
            master.implicitly_wait(10)

            # 验证跳转到拨号app
            # assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='电话']")
            # 验证号码正确
            # assert master.find_element(AppiumBy.ID, "com.samsung.android.dialer:id/digits").text == '+1 866-905-9950'

            # 切换回aosu app
            # 这种方式提示：java.lang.SecurityException: Permission Denial
            # master.start_activity('com.glazero.android', '.my.MyActivity')
            # 更换实现方式：KEYCODE_APP_SWITCH
            master.keyevent(187)
            time.sleep(1)
            master.keyevent(187)
            time.sleep(1)

        with allure.step('step5: 点击 英国电话'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/contact_number")[1].click()
            master.implicitly_wait(10)

            # 校验弹出拨打弹窗
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number")

        with allure.step('step6: 拨打电话'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number").click()
            master.implicitly_wait(10)

            # 验证跳转到拨号app
            # assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='电话']")
            # 验证号码正确
            # assert master.find_element(AppiumBy.ID, "com.samsung.android.dialer:id/digits").text == '+44 20 3885 0830'

            # 切换回aosu app
            master.keyevent(187)
            time.sleep(1)
            master.keyevent(187)
            time.sleep(1)

        with allure.step('step7: 点击 德国电话'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/contact_number")[2].click()
            master.implicitly_wait(10)

            # 校验弹出拨打弹窗
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number")

        with allure.step('step8: 拨打电话'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number").click()
            master.implicitly_wait(10)

            # 验证跳转到拨号app
            # assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='电话']")
            # 验证号码正确
            # assert master.find_element(AppiumBy.ID, "com.samsung.android.dialer:id/digits").text == '+49 32 221094692'

            # 切换回aosu app
            master.keyevent(187)
            time.sleep(1)
            master.keyevent(187)
            time.sleep(2)

        with allure.step('step9: 点击 日本电话'):
            master.find_elements(AppiumBy.ID, "com.glazero.android:id/contact_number")[3].click()
            master.implicitly_wait(10)

            # 校验弹出拨打弹窗
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number")

        with allure.step('step10: 拨打电话'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/contact_dial_number").click()
            master.implicitly_wait(10)

            # 验证跳转到拨号app
            # assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='电话']")
            # 验证号码正确
            # assert master.find_element(AppiumBy.ID, "com.samsung.android.dialer:id/digits").text == '+81 50-5840-2601'

            # 切换回aosu app
            master.keyevent(187)
            time.sleep(1)
            master.keyevent(187)
            time.sleep(2)

        with allure.step('step11: 点击左上角的返回按钮，退出联系我们页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

    @allure.story('关于')
    def test_about(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 关于 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[6].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="关于"]').click()
            master.implicitly_wait(10)

            # 页面加载完成后，校验页面的标题：关于
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '关于'

        with allure.step('step3: 检查 APP软件版本'):
            # 通过安装包获取app的版本号，例如，1.11.18.5119
            app_version_code = initPhone.get_app_version_name()

            # 从关于页面中看到的实际版本号：
            actual_version = master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_version").text
            master.implicitly_wait(10)

            # 校验版本号正确
            assert app_version_code in actual_version

        with allure.step('step4: 检查 所有设备SN号'):
            # 点击’查看所有设备SN号‘右侧的箭头
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_all_sn_arrow").click()
            master.implicitly_wait(10)

            # 通过api获取设备列表，用来判断，该页面展示什么
            devices_list = gz_public.get_devices_list()

            # 设备列表不为空时：
            if devices_list:
                # 校验页面的标题是：所有设备SN号
                assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '所有设备SN号'

                # 获取设备的所有sn 和name
                devices_list = gz_public.get_devices_list()

                from_api_get_dev_name = []
                from_api_get_dev_sn = []

                for device in devices_list:
                    from_api_get_dev_name.append(device["name"])
                    from_api_get_dev_sn.append(device["sn"])

                # 校验页面展示的设备名称在设备列表中
                for ii in range(0, len(from_api_get_dev_name)):
                    assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/tv_device_name")[
                               ii].text in from_api_get_dev_name

                # 校验页面展示的SN在设备列表中
                for ii in range(0, len(from_api_get_dev_sn)):
                    assert master.find_elements(AppiumBy.ID, "com.glazero.android:id/tv_device_sn")[
                               ii].text in from_api_get_dev_sn
            else:
                # 没有设备时校验页面中显示：暂无设备
                assert master.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='暂无设备']")

        with allure.step('step5: 点击 左上角的返回按钮，回到关于页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

        with allure.step('step6: 点击 相关协议'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/my_about_protocol").click()
            master.implicitly_wait(10)

            # 校验loading页面
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/webview_loading")

            # 页面加载时间较慢
            time.sleep(3)

            # 校验页面标题为：相关协议
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '相关协议'

        with allure.step('step7: 查看 相关协议'):
            # 在查看过程中查找：support@aosulife.com
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("support@aosulife.com"))')

            master.implicitly_wait(10)

        with allure.step('step8: 点击 左上角的返回按钮，回到关于页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

        with allure.step('step9: 点击 左上角的返回按钮，退出关于页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

    @allure.story('其他设置')
    def test_other_settings(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 其他设置 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[7].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="其他设置"]').click()
            master.implicitly_wait(10)

            # 校验loading页面
            # assert master.find_element(AppiumBy.ID, "com.glazero.android:id/webview_loading")

            # 页面加载完成后，校验页面的标题：相关协议
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '其他设置'

        with allure.step('step3: 查看 页面展示正确:展示 开启推荐 和 接收邮件资讯 2部分'):
            # 在查看过程中查找：开启推荐内容
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable('
                                                              'true)).scrollIntoView(new UiSelector().text('
                                                              '"开启推荐内容"))')

            # 在查看过程中查找：接收邮件资讯
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable('
                                                              'true)).scrollIntoView(new UiSelector().text('
                                                              '"接收邮件资讯"))')

            master.implicitly_wait(10)
            time.sleep(1)

        with allure.step('step4: 点击 左上角的返回按钮，退出 其他设置 页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
            master.implicitly_wait(10)

    @allure.story('相关协议')
    def test_agreement_terms(self):
        with allure.step('step1: 点击首页右上角的菜单按钮'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/img_menu").click()
            master.implicitly_wait(10)

            # 断言 进入了个人中心菜单
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/ivUserIcon").is_enabled() is True
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tvUserEmail").text == gz_public.email

        with allure.step('step2: 点击菜单中的 相关协议 项'):
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[7].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="相关协议"]').click()
            master.implicitly_wait(10)

            # 校验loading页面
            # assert master.find_element(AppiumBy.ID, "com.glazero.android:id/webview_loading")

            # 页面加载时间较慢
            time.sleep(3)

            # 页面加载完成后，校验页面的标题：相关协议
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title").text == '相关协议'

        with allure.step('step3: 查看 相关协议'):
            # 在查看过程中查找：support@aosulife.com
            master.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable('
                                                              'true)).scrollIntoView(new UiSelector().text('
                                                              '"support@aosulife.com"))')

            master.implicitly_wait(10)
            time.sleep(1)

        with allure.step('step4: 点击 左上角的返回按钮，退出 相关协议页面'):
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_back").click()
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
            # master.find_elements_by_id("com.glazero.android:id/tv_menu_item_name")[8].click()
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="退出登录"]').click()
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
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 500, "test_gzAndroidAuto.py::TestOpenFlow::test_v8p_open_flow",
    #              "--alluredir=./report/V8P"])

    # V8P 长时间开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_gzAndroidAuto.py::TestOpenFlow"
    #                                                   "::test_v8p_open_flow_long_time", "--alluredir=./report/V8P"])
    # 单挑执行回归用例，用于调试
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_regression.py::TestUserCenter::test_agreement_terms",
    #              "--alluredir=./report/regression"])
    # 整体执行
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_regression.py::TestGzLogin::test_gzLogin", "--alluredir=./report/regression"])
