import logging
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from gz_public import get_dsc
from gz_start_appium import StartAppium
import gz_public
import initPhone
import pytest
import allure
import time

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

#devices = ['Pixel 4 XL', 'TCL 10L', 'moto g', 'SamsungA51', 'moto_z4']
devices = ['SM-G781U', 'TCL 10L']

dev_tmp = []

android_package_name = 'com.glazero.android'


for device in devices:
    tmp = get_dsc(device=device)
    dev_tmp.append(tmp)


def setup_module():
    phone_1 = dev_tmp.pop(0)
    print('phone_1: ', phone_1)
    # phone_2 = dev_tmp.pop(0)
    # print('phone_2: ', phone_2)

    global master, slave

    StartAppium.start_appium(port=phone_1["port"])
    time.sleep(3)
    #master = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_1["port"], phone_1["des"])
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

class TestGzLogin(object):
    @staticmethod
    def setup_method():
        if master.current_activity != ".SplashActivity":
            master.activate_app(android_package_name)
            master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
        while (gz_public.isElementPresent(driver=master, by="id",
                                                  value="com.android.permissioncontroller:id/grant_dialog")) is True:
            master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="允许"]').click()
            time.sleep(2)

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
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/tv_title_string").text == "登录"

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
            # 点击登录按钮之后即进入首页后截图
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

@allure.feature('冷启app')
class Testapp_start(object):
    # @staticmethod
    # def setup_method():
    #     # if master.current_activity != ".SplashActivity":
    #     #     master.activate_app(android_package_name)
    #     #     master.wait_activity("com.glazero.android.SplashActivity", 2, 2)
    #         #判断一下屏幕是不是息屏了，如果息屏就点亮屏幕
    #         if not initPhone.isAwake():
    #             initPhone.keyEventSend(26)
    #         while (gz_public.isElementPresent(driver=master, by="id",
    #                                               value="com.android.permissioncontroller:id/grant_dialog")) is True:
    #             master.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="允许"]').click()
    #             time.sleep(2)
    #         # master.implicitly_wait(5)

    def test_startapp(self):
        with allure.step("step1:启动应用"):
            if not initPhone.isAwake():
                initPhone.keyEventSend(26)
            print("启动应用程序")
            #initPhone.applog()
            master.activate_app(android_package_name)  # 启动指定活动页面
            # 判断一下进入的界面是什么,如果没有登录就登录，如果登录过就下一步：
            while (gz_public.isElementPresent(driver=master, by="xpath",
                                              value='//android.widget.Button[@text="登录"]')) is True:
                TestGzLogin.test_gzLogin(self, gz_public.email, gz_public.pwd)
            time.sleep(2)
            # 对于判断场景进行查看，不成功的就上传保存
            if gz_public.isElementPresent(driver=master, by="xpath", value='//android.widget.TextView[@text="设置"]') != True:
                ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/regression0104/home_%s.png' % ts)
                time.sleep(2)
                allure.attach.file("./report/regression0104/home_%s.png" % ts, name="首页页面",attachment_type=allure.attachment_type.JPG)
            assert master.find_element(AppiumBy.ID,"com.glazero.android:id/tv_device_settings").text == "设置"

        with allure.step("step2:关闭APP"):
            if not initPhone.isAwake():
                initPhone.keyEventSend(26)
            print("关闭应用程序")
            master.terminate_app(android_package_name)  # 终止指定应用程序

@allure.feature("模拟手动冷启")
class Test_mockstart():
    def test_mockapp(self):
        with allure.step("step1:手动点击app启动"):
            if not initPhone.isAwake():
                initPhone.keyEventSend(26)
            #返回到设备主页
            initPhone.keyEventSend(3)
            print("启动应用程序")
            master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Aosu"]').click()
            while (gz_public.isElementPresent(driver=master, by="xpath",
                                              value='//android.widget.Button[@text="登录"]')) is True:
                TestGzLogin.test_gzLogin(self, gz_public.email, gz_public.pwd)
            time.sleep(2)
            # 对于判断场景进行查看，不成功的就上传保存
            if gz_public.isElementPresent(driver=master, by="xpath", value='//android.widget.TextView[@text="设置"]') != True:
                ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                master.save_screenshot('./report/regression0111/home_%s.png' % ts)
                time.sleep(2)
                allure.attach.file("./report/regression0111/home_%s.png" % ts, name="首页页面",attachment_type=allure.attachment_type.JPG)
            assert master.find_element(AppiumBy.ID,"com.glazero.android:id/tv_device_settings").text == "设置"

        with allure.step("step2：进入后台关闭app"):
            if not initPhone.isAwake():
                initPhone.keyEventSend(26)
            #进入手机后台界面
            initPhone.keyEventSend(187)
            #操作点击全部关闭按钮；
            master.find_element(AppiumBy.XPATH,'//android.widget.Button[@text="全部关闭"]').click()
            print("关闭应用程序")

        # def swipe_up(driver, duration=1000):
        #     # 获取屏幕大小
        #     screen_size = master.get_window_size()
        #
        #     # 计算起始点和终止点的坐标
        #     start_x = screen_size['width'] // 2
        #     start_y = screen_size['height'] * 3 // 4
        #     end_y = screen_size['height'] // 4
        #
        #     # 创建 TouchAction 对象
        #     touch = TouchAction(master)
        #
        #     # 执行向上滑动操作
        #     touch.press(x=start_x, y=start_y).wait(duration).move_to(x=start_x, y=end_y).release().perform()
        # try:
        #     # 等待应用加载
        #     time.sleep(5)
        #
        #     # 执行向上滑动操作，持续时间为1000毫秒（1秒）
        #     swipe_up(master, duration=1000)


    @staticmethod
    def teardown_class():
        master.terminate_app(android_package_name)
        master.implicitly_wait(10)


if __name__ == '__main__':
       pytest.main(["-q", "-s", "-ra", "--count=%d" % 1000, "test_mockapp.py::Test_mockstart::test_mockapp",
                    "--alluredir=./report/regression0111"])
