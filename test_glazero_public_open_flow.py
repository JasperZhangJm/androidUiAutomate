"""
----------------------------------
@Author: Liu shi jie
@Version: 2.0
@Date: 20240401
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
import os

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['moto g', 'Galaxy S10e', 'SamsungA51', 'moto_z4']

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

    # # 已安装aosu 先卸载
    # if initPhone.isAppExist():
    #     initPhone.uninstallApp()
    #
    # # 安装aosu app
    # initPhone.installApp()


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
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/smart_warn_tv_dialog_title").click()
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

        '''
        # 调试时关闭,正式执行时打开
        # 进入首页后检查，是否有智能提醒弹窗button-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 进入首页后检查，是否有低电量提醒弹窗-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 如果出现了固件升级的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/tv_dialog_ota_prompt_title") is True:
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '取消').click()
            master.implicitly_wait(10)
        '''

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
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:  #
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 进入首页后检查，是否有低电量提醒弹窗-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 如果出现了新人礼的弹窗，点击关闭按钮
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/img_ad") is True:
            master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
            master.implicitly_wait(10)

        '''
        # 调试时关闭,正式执行时打开
            
        # 进入首页后检查，是否有智能提醒弹窗button-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
            master.implicitly_wait(10)

        # 进入首页后检查，是否有低电量提醒弹窗-知道了
        while gz_public.isElementPresent(driver=master, by="id",
                                         value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
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
        '''

        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        兼容 一下固件升级的 弹窗
        '''

    def test_public_open_flow_result_portrait_screen_low_power(self, dev_model):

        # #######  重中之重：竖屏开流,低功耗设备,如:V8E  需要唤醒的设备，使用这个脚本

        """
        :前提条件：① 账号下要绑定 该 设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
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
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):

            # 先清除logcat,防止之前的日志数据,影响获取定位关键字.
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

            # 点击前面拿到的设备名称
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_model).click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            '''
            测试 C9S时开启,其他设备,不开启
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
            '''
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/%s/start_flow_%s.png' % (dev_model, start_flow))
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/%s/start_flow_%s.png" % (dev_model, start_flow), name="start flow",
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

                # 由于 V8E 开流页面是竖屏,所以日志中字段不一样.
                # 判断开流过程中,进入开流页面的状态，日志中出现字符串 LivePlaySingleFullFragment:onCreate 表示设备唤醒成功。
                create_LivePlay_fragment_state, create_LivePlay_fragment_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '开流播放片段在创建状态',
                    'BaseFragment',
                    'LivePlaySingleFullFragment:onCreate',
                    'LivePlaySingleFullFragment:onCreate', -2)

                print("开流播放片段在创建状态：%s" % create_LivePlay_fragment_state)

                # 进入开流页面失败时处理
                if create_LivePlay_fragment_state == 'LivePlaySingleFullFragment:onCreate':
                    print('开流播放片段在创建状态为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(
                        create_LivePlay_fragment_success_datatime,
                        click_time)
                    print("从点击屏幕开流 到 开流播放片段在创建 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 AJ列最后一行
                    colume_to_add_success = ['AJ']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 AB 列最后一行
                    colume_to_add_success = ['B']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert create_LivePlay_fragment_state == 'LivePlaySingleFullFragment:onCreate', "LivePlaySingleFullFragment:onCreate 表示设备唤醒成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    # 将 失败原因 和 失败分布,存储在 excel
                    if len(create_LivePlay_fragment_state) == 0:
                        print('开流播放片段在创建状态为: 空')
                        # 将从点击屏幕 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从点击屏幕 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['进入开流页面为空', '开始唤醒为空', '唤醒为空', 'p2p连接为空',
                                               'Preview 为空',
                                               '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流播放片段在创建状态为: 失败')
                        # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['进入开流页面失败', '开始唤醒失败', '唤醒失败', 'p2p连接失败',
                                                 'Preview 失败',
                                                 '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert create_LivePlay_fragment_state == 'LivePlaySingleFullFragment:onCreate', "LivePlaySingleFullFragment:onCreate 表示设备唤醒成功。"

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 表示设备唤醒成功。
                start_wake_state, start_wake_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '设备收到开始唤醒指令的状态是',
                    'TyCameraCenter',
                    'wakeStart',
                    'wakeStart', -1)

                print("设备收到开始唤醒指令的状态是：%s" % start_wake_state)

                # 设备唤醒失败时处理
                if start_wake_state == 'wakeStart':
                    print('设备收到开始唤醒指令为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(start_wake_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备收到开始唤醒指令 的时间差值: %s" % time_difference_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 AK列最后一行
                    colume_to_add_success = ['AK']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 AC 列最后一行
                    colume_to_add_success = ['C']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备收到开始唤醒指令为: 成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(start_wake_state) == 0:
                        print('设备收到开始唤醒指令为: 空')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的  'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的  'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['开始唤醒为空', '唤醒为空', 'p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('设备收到开始唤醒指令为: 失败')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['开始唤醒失败', '唤醒失败', 'p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备收到开始唤醒指令为: 成功。"

            with allure.step('step4-3: 进入开流页面，查看设备唤醒结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 表示设备唤醒成功。
                dev_wake_state, dev_wake_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '设备唤醒的结果是',
                    'TyCameraCenter',
                    'ensureDeviceWake wakeSuccess',
                    'wakeSuccess', -1)

                print("设备唤醒的结果是：%s" % dev_wake_state)

                # 设备唤醒失败时处理
                if dev_wake_state == 'wakeSuccess':
                    print('设备收到开始唤醒指令为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(dev_wake_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 获取到设备唤醒结果 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AL列最后一行
                    colume_to_add_success = ['AL']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AD 列最后一行
                    colume_to_add_success = ['D']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert dev_wake_state == 'wakeSuccess', "wakeSuccess 表示设备唤醒成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(dev_wake_state) == 0:
                        print('设备唤醒结果为: 空')
                        # 将从点击屏幕开流到设备唤醒成功的次数,存储在 ./data.xlsx 路径文件中的 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 B、C、D、E 列最后一行
                        colume_to_add_null = ['D', 'E', 'F', 'G']
                        content_to_add_null = ['唤醒为空', 'p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('设备唤醒结果为: 失败')
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 B、C、D、E 列最后一行
                        colume_to_add_failed = ['D', 'E', 'F', 'G']
                        content_to_add_failed = ['唤醒失败', 'p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-3-1: 冷启app。step时间点：%s'
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
                dev_p2p_state, dev_p2p_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '当前设备P2P状态是',
                    'TyCameraCenter',
                    'connectP2pEnd success',
                    'success', -1)
                print("当前设备P2P状态是：%s" % dev_p2p_state)

                # 设备唤醒失败时处理
                if dev_p2p_state == 'success':
                    print('设备P2P连接结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(dev_p2p_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备P2P连接结果 的时间差值: %s" % time_difference_success)

                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 AM 列最后一行
                    colume_to_add_success = ['AM']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 E  列最后一行
                    colume_to_add_success = ['E']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(dev_p2p_state) == 0:
                        print('P2P唤醒结果为: 空')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['E', 'F', 'G']
                        content_to_add_null = ['p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()
                    else:
                        print('P2P唤醒结果为: 失败')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['E', 'F', 'G']
                        content_to_add_failed = ['p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-4-1: 冷启app。step时间点：%s'
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
                play_state, play_state_success_datatime = gz_public.select_log_keyword_state_advanced('当前开流状态是',
                                                                                                      'LivePlayer',
                                                                                                      'state',
                                                                                                      'state:Playing',
                                                                                                      -1)
                print("当前开流状态是：%s" % play_state)

                # 开流失败时处理
                if play_state == 'state:Playing':
                    print('开流结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(play_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 获取到开流结果 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AN 列最后一行
                    colume_to_add_success = ['AN']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 F 列最后一行
                    colume_to_add_success = ['F']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert play_state == 'state:Playing', "state是Playing 开流成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(play_state) == 0:
                        print('开流结果为: 空')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_null = ['F', 'G']
                        content_to_add_null = ['Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流结果为: 失败')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AN', 'AO']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_failed = ['F', 'G']
                        content_to_add_failed = ['Preview 失败', '休眠失败']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                    colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-5-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert play_state == 'state:Playing', "state是Playing 开流成功。"

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            # 先清除logcat,防止之前的日志数据,影响获取定位关键字.
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            time.sleep(40)

            # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
            dev_dormancy_state, dev_dormancy_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                '当前设备休眠状态是',
                'dp_TyDeviceCenter',
                '\'\{\\"149\\":false\}\'',
                'dpStr={"149":false}', -1)
            print("当前设备休眠状态是：%s" % dev_dormancy_state)

            # 设备唤醒失败时处理
            if dev_dormancy_state == 'dpStr={"149":false}':
                print('设备休眠结果为: 成功')

                # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                time_difference_success = gz_public.time_difference_medium(dev_dormancy_state_success_datatime,
                                                                           click_time)
                print("从点击屏幕开流 到 获取到设备休眠结果 的时间差值: %s" % time_difference_success)

                # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                colume_to_add_success = ['AO']
                gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                colume_to_add_success = ['G']
                gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                        colume_to_add_success)

                assert dev_dormancy_state == 'dpStr={"149":false}', "'dpStr={\"149\":false}' 表示设备休眠成功。"
            else:
                # 将 APP和涂鸦日志，上传到 HTML上
                gz_public.log_upload_html(dev_model)
                master.implicitly_wait(10)

                if len(dev_dormancy_state) == 0:
                    print('设备休眠结果为: 空')
                    # 将 从点击屏幕返回 到 设备休眠成功 的次数,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                    colume_to_add_null = ['AO']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                    colume_to_add_null = ['G']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', '休眠状态为空', colume_to_add_null)
                    # 获取完成后清除logcat
                    r_obj = os.popen("adb logcat -c")
                    r_obj.close()

                else:
                    print('设备休眠结果为: 失败')
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                    colume_to_add_failed = ['AO']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                    colume_to_add_failed = ['G']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', '休眠失败', colume_to_add_failed)
                    # 获取完成后清除logcat
                    r_obj = os.popen("adb logcat -c")
                    r_obj.close()

                with allure.step('step5-1-1: 冷启app。step时间点：%s'
                                 % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                    # appium 1.22.2的用方法
                    # master.close_app()
                    master.terminate_app(android_package_name)
                    master.implicitly_wait(10)

                # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                assert dev_dormancy_state == 'dpStr={"149":false}', "dpStr={\"149\":false} 表示设备休眠成功。"

            # 进入首页后检查，是否有智能提醒弹窗button-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 进入首页后检查，是否有低电量提醒弹窗-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 如果出现了固件升级的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/tv_dialog_ota_prompt_title") is True:
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '取消').click()
                master.implicitly_wait(10)

            # 如果出现了新人礼的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/img_ad") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
                master.implicitly_wait(10)

                # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

    def test_public_open_flow_result_landscape_screen_nonLowPower(self, dev_model):
        #  #######  重中之重：非低功耗设备,如:套包、长电 这些不需要唤醒的设备，使用这个脚本

        """
        :前提条件：① 账号下要绑定C9E设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
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
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):

            # 先清除logcat,防止之前的日志数据,影响获取定位关键字.
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

            # 点击前面拿到的设备名称
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_model).click()

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

            '''
            测试 C9S时开启,其他设备,不开启
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
            '''
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/%s/start_flow_%s.png' % (dev_model, start_flow))
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/%s/start_flow_%s.png" % (dev_model, start_flow), name="start flow",
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
                # 判断开流过程中,进入开流页面的状态，日志中出现字符串 LivePlaySingleFragment:onCreate 表示设备唤醒成功。
                create_LivePlay_fragment_state, create_LivePlay_fragment_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '开流播放片段在创建状态',
                    'BaseFragment',
                    'LivePlaySingleFragment:onCreate',
                    'LivePlaySingleFragment:onCreate', -2)

                print("开流播放片段在创建状态：%s" % create_LivePlay_fragment_state)

                # 进入开流页面失败时处理
                if create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate':
                    print('开流播放片段在创建状态为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(
                        create_LivePlay_fragment_success_datatime,
                        click_time)
                    print("从点击屏幕开流 到 开流播放片段在创建 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 AJ列最后一行
                    colume_to_add_success = ['AJ']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 AB 列最后一行
                    colume_to_add_success = ['B']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备唤醒成功。"
                else:
                    '''
                    因为 APP包，原有日志保存路径换了，导致取不了 app日志，所以先注释掉。等开发改完，再取消注释。
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)         
                    '''

                    # 将 失败原因 和 失败分布,存储在 excel
                    if len(create_LivePlay_fragment_state) == 0:
                        print('开流播放片段在创建状态为: 空')
                        # 将从点击屏幕 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从点击屏幕 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['进入开流页面为空', '开始唤醒为空', '唤醒为空', 'p2p连接为空',
                                               'Preview 为空',
                                               '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流播放片段在创建状态为: 失败')
                        # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['进入开流页面失败', '开始唤醒失败', '唤醒失败', 'p2p连接失败',
                                                 'Preview 失败',
                                                 '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert create_LivePlay_fragment_state == 'LivePlayFragment:onCreate', "LivePlayFragment:onCreate 表示设备唤醒成功。"

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 表示设备唤醒成功。
                start_wake_state, start_wake_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '设备收到开始唤醒指令的状态是',
                    'TyCameraCenter',
                    'wakeStart',
                    'wakeStart', -1)

                print("设备收到开始唤醒指令的状态是：%s" % start_wake_state)

                # 设备唤醒失败时处理
                if start_wake_state == 'ensureDeviceWake->wakeStart':
                    print('设备收到开始唤醒指令为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(start_wake_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备收到开始唤醒指令 的时间差值: %s" % time_difference_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 AK列最后一行
                    colume_to_add_success = ['AK']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 AC 列最后一行
                    colume_to_add_success = ['C']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert start_wake_state == 'ensureDeviceWake->wakeStart', "ensureDeviceWake->wakeStart 表示设备成功收到开始唤醒指令。"
                else:
                    '''
                    因为 APP包，原有日志保存路径换了，导致取不了 app日志，所以先注释掉。等开发改完，再取消注释。
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)         
                    '''

                    if len(start_wake_state) == 0:
                        print('设备收到开始唤醒指令为: 空')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的  'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的  'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['开始唤醒为空', '唤醒为空', 'p2p连接为空', 'Preview 为空',
                                               '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('设备收到开始唤醒指令为: 失败')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['开始唤醒失败', '唤醒失败', 'p2p连接失败', 'Preview 失败',
                                                 '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert start_wake_state == 'ensureDeviceWake->wakeStart', "ensureDeviceWake->wakeStart 表示设备成功收到开始唤醒指令为。"

            with allure.step('step4-3: 进入开流页面，查看P2P连接结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
                dev_p2p_state, dev_p2p_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '当前设备P2P状态是',
                    'TyCameraCenter',
                    'connectP2pEnd success',
                    'success', -1)
                print("当前设备P2P状态是：%s" % dev_p2p_state)

                # 设备唤醒失败时处理
                if dev_p2p_state == 'success':
                    print('设备P2P连接结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(dev_p2p_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备P2P连接结果 的时间差值: %s" % time_difference_success)

                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 AM 列最后一行
                    colume_to_add_success = ['AM']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 E  列最后一行
                    colume_to_add_success = ['E']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"
                else:
                    '''
                    因为 APP包，原有日志保存路径换了，导致取不了 app日志，所以先注释掉。等开发改完，再取消注释。
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)         
                    '''

                    if len(dev_p2p_state) == 0:
                        print('P2P唤醒结果为: 空')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['E', 'F', 'G']
                        content_to_add_null = ['p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()
                    else:
                        print('P2P唤醒结果为: 失败')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['E', 'F', 'G']
                        content_to_add_failed = ['p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-3-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"

            with allure.step('step4-4: 进入开流页面，查看开流结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                # 判断开流结果，加载过程消失后开流成功或者失败
                play_state, play_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '当前开流状态是',
                    'LivePlayer',
                    'state',
                    'state:Playing',
                    -1)
                print("当前开流状态是：%s" % play_state)

                # 开流失败时处理
                if play_state == 'state:Playing':
                    print('开流结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(play_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 获取到开流结果 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AN 列最后一行
                    colume_to_add_success = ['AN']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 F 列最后一行
                    colume_to_add_success = ['F']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert play_state == 'state:Playing', "state是Playing 开流成功。"
                else:
                    '''
                    因为 APP包，原有日志保存路径换了，导致取不了 app日志，所以先注释掉。等开发改完，再取消注释。
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)         
                    '''

                    if len(play_state) == 0:
                        print('开流结果为: 空')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_null = ['F', 'G']
                        content_to_add_null = ['Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流结果为: 失败')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AN', 'AO']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_failed = ['F', 'G']
                        content_to_add_failed = ['Preview 失败', '休眠失败']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                    colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-4-1: 冷启app。step时间点：%s'
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

            # 进入首页后检查，是否有智能提醒弹窗button-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 进入首页后检查，是否有低电量提醒弹窗-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 如果出现了固件升级的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/tv_dialog_ota_prompt_title") is True:
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '取消').click()
                master.implicitly_wait(10)

            # 如果出现了新人礼的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/img_ad") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
                master.implicitly_wait(10)

                # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

    def test_public_open_flow_result_landscape_screen_low_power(self, dev_model):

        # #######  重中之重：低功耗设备,如:C6L、C9L、C9E、C9S 等 需要唤醒的设备，使用这个脚本

        """
        :前提条件：① 账号下要绑定C9E设备；② 关闭消息通知，不要弹push，会遮挡按钮的点击
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
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(10)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step3: 点击前面拿到的设备名称，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):

            # 先清除logcat,防止之前的日志数据,影响获取定位关键字.
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

            # 点击前面拿到的设备名称
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % dev_model).click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            master.implicitly_wait(10)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step4: 进入开流页面，查看开流结果。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            '''
            # 调试时关闭,正式执行时打开
            
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
            '''

            '''
            测试 C9S时开启,其他设备,不开启
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
            '''
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)

            # 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/%s/start_flow_%s.png' % (dev_model, start_flow))
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/%s/start_flow_%s.png" % (dev_model, start_flow), name="start flow",
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
                # 判断开流过程中,进入开流页面的状态，日志中出现字符串 LivePlaySingleFragment:onCreate 表示设备唤醒成功。
                create_LivePlay_fragment_state, create_LivePlay_fragment_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '开流播放片段在创建状态',
                    'BaseFragment',
                    'LivePlaySingleFragment:onCreate',
                    'LivePlaySingleFragment:onCreate', -2)

                print("开流播放片段在创建状态：%s" % create_LivePlay_fragment_state)

                # 进入开流页面失败时处理
                if create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate':
                    print('开流播放片段在创建状态为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(
                        create_LivePlay_fragment_success_datatime,
                        click_time)
                    print("从点击屏幕开流 到 开流播放片段在创建 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 AJ列最后一行
                    colume_to_add_success = ['AJ']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 AB 列最后一行
                    colume_to_add_success = ['B']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert create_LivePlay_fragment_state == 'LivePlaySingleFragment:onCreate', "LivePlaySingleFragment:onCreate 表示设备唤醒成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    # 将 失败原因 和 失败分布,存储在 excel
                    if len(create_LivePlay_fragment_state) == 0:
                        print('开流播放片段在创建状态为: 空')
                        # 将从点击屏幕 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从点击屏幕 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['进入开流页面为空', '开始唤醒为空', '唤醒为空', 'p2p连接为空',
                                               'Preview 为空',
                                               '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流播放片段在创建状态为: 失败')
                        # 将从点击屏幕开流 到 进入开流页面 的次数,存储在 ./data.xlsx 路径文件中的 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流 到 进入开流页面 的时间,存储在 ./data.xlsx 路径文件中的 'B', 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['B', 'C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['进入开流页面失败', '开始唤醒失败', '唤醒失败', 'p2p连接失败',
                                                 'Preview 失败',
                                                 '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-1-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert create_LivePlay_fragment_state == 'LivePlayFragment:onCreate', "LivePlayFragment:onCreate 表示设备唤醒成功。"

            with allure.step('step4-2: 进入开流页面，查看设备接收到唤醒指令结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 表示设备唤醒成功。
                start_wake_state, start_wake_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '设备收到开始唤醒指令的状态是',
                    'TyCameraCenter',
                    'wakeStart',
                    'wakeStart', -1)

                print("设备收到开始唤醒指令的状态是：%s" % start_wake_state)

                # 设备唤醒失败时处理
                if start_wake_state == 'wakeStart':
                    print('设备收到开始唤醒指令为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(start_wake_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备收到开始唤醒指令 的时间差值: %s" % time_difference_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 AK列最后一行
                    colume_to_add_success = ['AK']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)

                    # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 AC 列最后一行
                    colume_to_add_success = ['C']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备收到开始唤醒指令为: 成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(start_wake_state) == 0:
                        print('设备收到开始唤醒指令为: 空')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的  'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的  'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_null = ['开始唤醒为空', '唤醒为空', 'p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('设备收到开始唤醒指令为: 失败')
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的次数,存储在 ./data.xlsx 路径文件中的 'AK', 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AK', 'AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从 点击屏幕开流 到 设备收到 开始唤醒时 的时间,存储在 ./data.xlsx 路径文件中的 'C', 'D', 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['C', 'D', 'E', 'F', 'G']
                        content_to_add_failed = ['开始唤醒失败', '唤醒失败', 'p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-2-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert start_wake_state == 'wakeStart', "wakeStart 表示设备收到开始唤醒指令为: 成功。"

            with allure.step('step4-3: 进入开流页面，查看设备唤醒结果。step时间点：%s'
                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

                # 判断开流过程中,设备接收到 开始唤醒指令 的状态，日志中出现字符串 ensureDeviceWake 表示设备唤醒成功。
                dev_wake_state, dev_wake_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '设备唤醒的结果是',
                    'TyCameraCenter',
                    'ensureDeviceWake wakeSuccess',
                    'wakeSuccess', -1)

                print("设备唤醒的结果是：%s" % dev_wake_state)

                # 设备唤醒失败时处理
                if dev_wake_state == 'wakeSuccess':
                    print('设备收到开始唤醒指令为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(dev_wake_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 获取到设备唤醒结果 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AL列最后一行
                    colume_to_add_success = ['AL']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AD 列最后一行
                    colume_to_add_success = ['D']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert dev_wake_state == 'wakeSuccess', "wakeSuccess 表示设备唤醒成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(dev_wake_state) == 0:
                        print('设备唤醒结果为: 空')
                        # 将从点击屏幕开流到设备唤醒成功的次数,存储在 ./data.xlsx 路径文件中的 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_list_to_add_null = ['AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_list_to_add_null)
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 B、C、D、E 列最后一行
                        colume_to_add_null = ['D', 'E', 'F', 'G']
                        content_to_add_null = ['唤醒为空', 'p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('设备唤醒结果为: 失败')
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 'AL', 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AL', 'AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 B、C、D、E 列最后一行
                        colume_to_add_failed = ['D', 'E', 'F', 'G']
                        content_to_add_failed = ['唤醒失败', 'p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)

                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-3-1: 冷启app。step时间点：%s'
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
                dev_p2p_state, dev_p2p_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                    '当前设备P2P状态是',
                    'TyCameraCenter',
                    'connectP2pEnd success',
                    'success', -1)
                print("当前设备P2P状态是：%s" % dev_p2p_state)

                # 设备唤醒失败时处理
                if dev_p2p_state == 'success':
                    print('设备P2P连接结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(dev_p2p_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 设备P2P连接结果 的时间差值: %s" % time_difference_success)

                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 AM 列最后一行
                    colume_to_add_success = ['AM']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 E  列最后一行
                    colume_to_add_success = ['E']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert dev_p2p_state == 'success', "success 表示设备p2p连接成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(dev_p2p_state) == 0:
                        print('P2P唤醒结果为: 空')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_null = ['E', 'F', 'G']
                        content_to_add_null = ['p2p连接为空', 'Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()
                    else:
                        print('P2P唤醒结果为: 失败')
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的次数,存储在 ./data.xlsx 路径文件中的 'AM', 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AM', 'AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将 从点击屏幕开流 到 p2p唤醒成功 的时间,存储在 ./data.xlsx 路径文件中的 'E', 'F', 'G' 列最后一行
                        colume_to_add_failed = ['E', 'F', 'G']
                        content_to_add_failed = ['p2p连接失败', 'Preview 失败', '休眠失败']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                              colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-4-1: 冷启app。step时间点：%s'
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
                play_state, play_state_success_datatime = gz_public.select_log_keyword_state_advanced('当前开流状态是',
                                                                                                      'LivePlayer',
                                                                                                      'state',
                                                                                                      'state:Playing',
                                                                                                      -1)
                print("当前开流状态是：%s" % play_state)

                # 开流失败时处理
                if play_state == 'state:Playing':
                    print('开流结果为: 成功')

                    # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                    time_difference_success = gz_public.time_difference_medium(play_state_success_datatime,
                                                                               click_time)
                    print("从点击屏幕开流 到 获取到开流结果 的时间差值: %s" % time_difference_success)

                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 AN 列最后一行
                    colume_to_add_success = ['AN']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                    # 将从点击屏幕开流到设备唤醒成功的时间,存储在 ./data.xlsx 路径文件中的 F 列最后一行
                    colume_to_add_success = ['F']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                            colume_to_add_success)

                    assert play_state == 'state:Playing', "state是Playing 开流成功。"
                else:
                    # 将 APP和涂鸦日志，上传到 HTML上
                    gz_public.log_upload_html(dev_model)
                    master.implicitly_wait(10)

                    if len(play_state) == 0:
                        print('开流结果为: 空')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_null = ['AN', 'AO']
                        gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_null = ['F', 'G']
                        content_to_add_null = ['Preview 为空', '休眠为空']
                        gz_public.result_save_excel_full_list('./data.xlsx', 'Sheet1', content_to_add_null,
                                                              colume_to_add_null)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    else:
                        print('开流结果为: 失败')
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'AN', 'AO' 列最后一行
                        colume_to_add_failed = ['AN', 'AO']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                        # 将从点击屏幕开流到设备第一帧画面成功回来的时间,存储在 ./data.xlsx 路径文件中的 'F', 'G' 列最后一行
                        colume_to_add_failed = ['F', 'G']
                        content_to_add_failed = ['Preview 失败', '休眠失败']
                        gz_public.result_save_excel('./data.xlsx', 'Sheet1', content_to_add_failed,
                                                    colume_to_add_failed)
                        # 获取完成后清除logcat
                        r_obj = os.popen("adb logcat -c")
                        r_obj.close()

                    with allure.step('step4-5-1: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.terminate_app(android_package_name)
                        master.implicitly_wait(10)

                    # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                    assert play_state == 'state:Playing', "state是Playing 开流成功。"

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):

            # 先清除logcat,防止之前的日志数据,影响获取定位关键字.
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

            # 点击左上角的 返回按钮
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            time.sleep(40)

            # 判断开流过程中,设备唤醒状态，日志中出现字符串 ensureDeviceWake wakeSuccess 表示设备唤醒成功。
            dev_dormancy_state, dev_dormancy_state_success_datatime = gz_public.select_log_keyword_state_advanced(
                '当前设备休眠状态是',
                'dp_TyDeviceCenter',
                '\'\{\\"149\\":false\}\'',
                'dpStr={"149":false}', -1)
            print("当前设备休眠状态是：%s" % dev_dormancy_state)

            # 设备唤醒失败时处理
            if dev_dormancy_state == 'dpStr={"149":false}':
                print('设备休眠结果为: 成功')

                # 计算  从点击屏幕返回 到 设备休眠成功 的时间差值
                time_difference_success = gz_public.time_difference_medium(dev_dormancy_state_success_datatime,
                                                                           click_time)
                print("从点击屏幕开流 到 获取到设备休眠结果 的时间差值: %s" % time_difference_success)

                # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                colume_to_add_success = ['AO']
                gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 1, colume_to_add_success)
                # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                colume_to_add_success = ['G']
                gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', time_difference_success,
                                                        colume_to_add_success)

                assert dev_dormancy_state == 'dpStr={"149":false}', "'dpStr={\"149\":false}' 表示设备休眠成功。"
            else:
                # 将 APP和涂鸦日志，上传到 HTML上
                gz_public.log_upload_html(dev_model)
                master.implicitly_wait(10)

                if len(dev_dormancy_state) == 0:
                    print('设备休眠结果为: 空')
                    # 将 从点击屏幕返回 到 设备休眠成功 的次数,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                    colume_to_add_null = ['AO']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_null)
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                    colume_to_add_null = ['G']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', '休眠状态为空', colume_to_add_null)
                    # 获取完成后清除logcat
                    r_obj = os.popen("adb logcat -c")
                    r_obj.close()

                else:
                    print('设备休眠结果为: 失败')
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 'AO' 列最后一行
                    colume_to_add_failed = ['AO']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', 0, colume_to_add_failed)
                    # 将 从点击屏幕返回 到 设备休眠成功 的时间,存储在 ./data.xlsx 路径文件中的 G 列最后一行
                    colume_to_add_failed = ['G']
                    gz_public.result_save_excel_column_list('./data.xlsx', 'Sheet1', '休眠失败', colume_to_add_failed)
                    # 获取完成后清除logcat
                    r_obj = os.popen("adb logcat -c")
                    r_obj.close()

                with allure.step('step5-1-1: 冷启app。step时间点：%s'
                                 % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                    # appium 1.22.2的用方法
                    # master.close_app()
                    master.terminate_app(android_package_name)
                    master.implicitly_wait(10)

                # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                assert dev_dormancy_state == 'dpStr={"149":false}', "dpStr={\"149\":false} 表示设备休眠成功。"

            # 进入首页后检查，是否有智能提醒弹窗button-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 进入首页后检查，是否有低电量提醒弹窗-知道了
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
                master.implicitly_wait(10)

            # 如果出现了固件升级的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/tv_dialog_ota_prompt_title") is True:
                master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '取消').click()
                master.implicitly_wait(10)

            # 如果出现了新人礼的弹窗，点击关闭按钮
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/img_ad") is True:
                master.find_element(AppiumBy.ID, "com.glazero.android:id/iv_close").click()
                master.implicitly_wait(10)

                # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

            # 获取完成后清除logcat
            r_obj = os.popen("adb logcat -c")
            r_obj.close()

    # 重中之重 #############################################
    # 适用: 第一类：竖屏 低功耗设备 + 门铃 V8E  需要：休眠 和 唤醒成功 的指令
    @allure.title('V8E 多次开流 ')
    @allure.story('用户循环测试V8E的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠 各节点用时时间 ')
    def test_v8e_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_portrait_screen_low_power 的代码即可
        self.test_public_open_flow_result_portrait_screen_low_power('V8E')

    #  适用: 第二类：横屏 长电设备 + 套包设备 + 门铃 V8S、V8P  不需要休眠、唤醒成功的指令
    @allure.title('V8P 多次开流 ')
    @allure.story('用户循环测试V8P的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_v8p_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('V8P')

    @allure.title('V8S 多次开流 ')
    @allure.story('用户循环测试V8S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_v8s_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('V8S')

    @allure.title('C2E 多次开流 ')
    @allure.story('用户循环测试C2E的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c2e_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C2E')

    @allure.title('C4L 多次开流 ')
    @allure.story('用户循环测试C4L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c4l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C4L')

    @allure.title('C5L 多次开流 ')
    @allure.story('用户循环测试C5L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c5l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C5L')

    @allure.title('C5E 多次开流 ')
    @allure.story('用户循环测试C5E的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c5e_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C5E')

    @allure.title('L5P 多次开流 ')
    @allure.story('用户循环测试L5P的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_l5p_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('L5P')

    @allure.title('C6P 多次开流 ')
    @allure.story('用户循环测试C6P的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c6p_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C6P')

    @allure.title('C6S 多次开流 ')
    @allure.story('用户循环测试C6S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c6s_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C6S')

    @allure.title('C7P 多次开流 ')
    @allure.story('用户循环测试C7P的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c7p_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C7P')

    @allure.title('C7S 多次开流 ')
    @allure.story('用户循环测试C7S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c7s_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C7S')

    @allure.title('C8E 多次开流 ')
    @allure.story('用户循环测试C8E的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c8e_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C8E')

    @allure.title('C9C3CA11 多次开流 ')
    @allure.story('用户循环测试C7S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview 各节点用时时间 ')
    def test_c9c3ca11_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_nonLowPower 的代码即可
        self.test_public_open_flow_result_landscape_screen_nonLowPower('C9C3CA11')

    # 适用: 第三类： 横屏  低功耗设备 + V8S、V8P
    @allure.title('C6L 多次开流 ')
    @allure.story('用户循环测试C6L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c6l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C6L')

    @allure.title('C7L 多次开流 ')
    @allure.story('用户循环测试C7L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c7l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C7L')

    @allure.title('C8L 多次开流 ')
    @allure.story('用户循环测试C8L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c8l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C8L')

    @allure.title('C8S 多次开流 ')
    @allure.story('用户循环测试C8S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c8s_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C8S')
    @allure.title('C9L 多次开流 ')
    @allure.story('用户循环测试C9L的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c9l_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C9L')

    @allure.title('C9S 多次开流 ')
    @allure.story('用户循环测试C9S的开流-关流，即多次开流，结果输出:唤醒、p2p、Preview、休眠各节点用时时间 ')
    def test_c9s_open_flow_result(self):
        # 直接调用 test_public_open_flow_result_landscape_screen_low_power 的代码即可
        self.test_public_open_flow_result_landscape_screen_low_power('C9S')


if __name__ == '__main__':
    # 重中之重 #############################################
    # 适用: 第一类：竖屏 低功耗设备 + 门铃 V8E  需要：休眠 和 唤醒成功 的指令
    # V8E 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_v8e_open_flow_result",
    #      "--alluredir=./report/V8E"])

    #  适用: 第二类：横屏 长电设备 + 套包设备 + 门铃 V8S、V8P  不需要休眠、唤醒成功的指令
    # V8P 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_v8p_open_flow_result",
    #              "--alluredir=./report/V8P"])

    # V8S 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_v8s_open_flow_result",
    #              "--alluredir=./report/V8S"])

    # C2E 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c2e_open_flow_result",
    #              "--alluredir=./report/C2E"])

    # C4L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c4l_open_flow_result",
    #              "--alluredir=./report/C4L"])

    # C5L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c5l_open_flow_result",
    #              "--alluredir=./report/C5L"])

    # C5E 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c5e_open_flow_result",
    #              "--alluredir=./report/C5E"])

    # L5P 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_live_play_c7p_demo.py::TestOpenFlow::test_l5p_open_flow_result",
    #              "--alluredir=./report/L5P"])

    # C6P 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c6p_open_flow_result",
    #              "--alluredir=./report/C6P"])

    # C6S 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c6s_open_flow_result",
    #              "--alluredir=./report/C6S"])

    # C7P 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_glazero_public_open_flow.py::TestOpenFlow::test_c7p_open_flow_result",
    #              "--alluredir=./report/C7P"])

    # C7S 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c7s_open_flow_result",
    #              "--alluredir=./report/C7S"])

    # C8E 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_glazero_public_open_flow.py::TestOpenFlow::test_c8e_open_flow_result",
    #              "--alluredir=./report/C8E"])

    # C9C套包  C9C3CA11 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c9c3ca11_open_flow_result",
    #              "--alluredir=./report/C9C3CA11"])

    # 适用: 第三类： 横屏  低功耗设备 + V8S、V8P
    # C6L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c6l_open_flow_result",
    #              "--alluredir=./report/C6L"])

    # C7L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c7l_open_flow_result",
    #              "--alluredir=./report/C7L"])

    # C8L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c8l_open_flow_result",
    #              "--alluredir=./report/C8L"])

    # C8S 多次开流 包含 Excel 报告
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_glazero_public_open_flow.py::TestOpenFlow::test_c8s_open_flow_result",
                 "--alluredir=./report/C8S"])

    # C9L 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c9l_open_flow_result",
    #              "--alluredir=./report/C9L"])

    # C9E 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 1, "test_glazero_public_open_flow.py::TestOpenFlow::test_c9e_open_flow_result",
    #              "--alluredir=./report/C9E"])

    # C9S 多次开流 包含 Excel 报告
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_glazero_public_open_flow.py::TestOpenFlow::test_c9s_open_flow_result",
    #              "--alluredir=./report/C9S"])
