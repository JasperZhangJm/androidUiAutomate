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
import os

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
from tqdm import tqdm
from datetime import datetime
# import datetime
import re
import psutil

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['Pixel 7', 'Pixel 4', 'Samsung S22', 'moto g', 'Samsung S8', 'SamsungSCV36', 'SamsungA51', 'moto_z4']

dev_tmp = []
# 慧云通讯 App 包名
android_package_name = 'com.huiyun.care.viewerpro'
devices_name = '99051FFBA006Z2'

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
    # time.sleep(3)
    # master = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_1["port"], phone_1["des"])
    master = webdriver.Remote("http://127.0.0.1:%s" % phone_2["port"], phone_2["des"])

    master.implicitly_wait(10)

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


def teardown_module():
    master.quit()
    # slave.quit()


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
    def setup_method(self):
        # 检查屏幕是否点亮
        if not initPhone.isAwake():
            # 26 电源键
            initPhone.keyEventSend(26)
            time.sleep(1)

        # 进入首页后检查，是否有智能提醒弹窗button-知道了
        # while gz_public.isElementPresent(driver=master, by="id",
        #                                  value="com.glazero.android:id/smart_warn_tv_dialog_title") is True:
        #     master.find_element(AppiumBy.ID, 'com.glazero.android:id/button').click()
        #     master.implicitly_wait(10)
        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        '''
        # 不在首页的话 启动一下app
        if gz_public.isElementPresent(driver=master, by="id", value="com.huiyun.care.viewerpro:id/logo") is False:
            # appium1.22.2的用法
            # master.launch_app()
            master.activate_app(android_package_name)
            master.wait_activity("com.huiyun.care.viewer.ad.AdvertisingActivity", 2, 2)
            time.sleep(10)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.huiyun.care.viewerpro:id/logo") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        '''

    def test_public_open_flow_result(self, dev_model):
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
        # 执行用例的次数,保存到Excel中.
        colume_to_add_success = ['N']
        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
                                                colume_to_add_success)
        master.implicitly_wait(10)

        # 获取 当前设备的 设备名
        dev_name = master.find_element(AppiumBy.ID, 'com.huiyun.care.viewerpro:id/device_name').text
        # 获取设备的名字
        print("找到的设备名称是：%s，设备型号是：%s" % (dev_name, dev_model))

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，%s。step时间点：%s'
                         % (dev_name, datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3])):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(20)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2: 点击前面拿到的设备屏幕,开始开流，例如，%s。step时间点：%s'
                         % (dev_name, datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3])):

            time.sleep(5)
            # 点击屏幕开流
            master.find_element(AppiumBy.ID, 'com.huiyun.care.viewerpro:id/device_screenshot').click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            time.sleep(1)

        with allure.step('step3: 进入开流页面，查看开流结果。step时间点：%s'
                         % datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3]):
            # 出现加载动画，一共4个，依次为：①正在建立访问通道...②正在连接网络服务...③实时视频加载中...④加载较慢，尝试切换至流畅模式
            # resource-id相同：com.glazero.android:id/tv_live_play_loading
            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒

            # 声明一个 空 list列表,本次截图路径 和 截图时间 ,以提供给下下面 for循环 提取每次截图中的 左上角时间戳 和 当时时间,
            Screenshot_path_and_time_list = []

            # 获取当前时间
            start_live_play_time = datetime.now()
            print(start_live_play_time)

            # 800 ms 截一张图,持续 10秒,共截取 12张图.
            for ii in range(1, 13):
                # 截一张图
                start_flow = datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3]
                start_image_save_path = './report/Ring/%s_start_flow_%s.png' % (ii, start_flow)
                master.save_screenshot(start_image_save_path)

                # 将 本次截图路径 和 截图时间 保存到 list列表: Screenshot_path_and_time_list 中,以提供给下面 for循环 提取每次截图中的 左上角时间戳 和 当时时间,
                Screenshot_path_and_time_list.append([start_image_save_path, start_flow])

                ii = ii + 1

            # 获取当前时间
            end_live_play_time = datetime.now()
            print(end_live_play_time)
            diff_time = end_live_play_time - start_live_play_time
            print('12次 截图所用时间 %s ' % diff_time)

            for jj in range(1, len(Screenshot_path_and_time_list) + 1):
                # 从 Screenshot_path_and_time_list 列表中中 取出每次截图,来识别 左上角时间戳
                start_image_save_path = Screenshot_path_and_time_list[jj - 1][0]

                # 提取开流页面,左上角的时间戳.
                # 将 本次开流截图,转成黑白色,并且保存到 路径  image_black_and_white_path_name  中
                image_black_and_white_path_name = './report/Ring/%s_start_flow_%s.png' % (jj, start_flow)
                # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中
                image_partial_path_name = './report/Ring/%s-1_start_flow_%s.png' % (jj, start_flow)
                # 将 本次开流截图,转成黑白色,并且保存到 路径  image_black_and_white_path_name  中
                gz_public.picture_contrast_black_and_white(start_image_save_path,
                                                           image_black_and_white_path_name)
                # # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中,并且识别 其中的文字 传给start_extracted_text. 手机 三星S8
                # start_extracted_text = gz_public.get_image_text_simple(image_black_and_white_path_name, 0, 0, 210,
                #                                                        380, 240, image_partial_path_name)

                # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中,并且识别 其中的文字 传给start_extracted_text
                start_extracted_text = gz_public.get_image_text_simple(image_black_and_white_path_name, 0, 0, 280,
                                                                       500, 350, image_partial_path_name)  # 手机 pixel 4xl

                # # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中,并且识别 其中的文字 传给start_extracted_text
                # start_extracted_text = gz_public.get_image_text_simple(image_black_and_white_path_name, 0, 0, 370,
                #                                                        500, 420,
                #                                                        image_partial_path_name)  # 手机 Samsung S22

                print(start_extracted_text)

                # 例: dan.08.2024 20:18:27
                if start_extracted_text != "":
                    if ":" in start_extracted_text and "-" in start_extracted_text:

                        # 将 开流成功的 截图上传到 HTML 报告中.
                        allure.attach.file(start_image_save_path, name="%s_start_flow_success_%s" % (jj, start_flow),
                                           attachment_type=allure.attachment_type.JPG)
                        master.implicitly_wait(10)

                        # 从 Screenshot_path_and_time_list 列表中中 取出每次截图,来识别 左上角时间戳
                        success_live_play_time_str = Screenshot_path_and_time_list[jj - 1][1]  # 例: 2024-01-02_10,10,10

                        # 将 success_live_play_time 字符串 格式 整理成 时间格式
                        success_live_play_time_str = success_live_play_time_str.replace("_", " ").replace(",", ":")
                        print(success_live_play_time_str)

                        # 将 开流成功截图 时间 转化成 datetime类型,用于下面时间相减
                        success_live_play_time = gz_public.string_change_datetime(success_live_play_time_str)
                        print('开流成功时间', success_live_play_time)

                        # 计算 从点击屏幕到开流成功 的时间差.
                        different_time = success_live_play_time - click_time
                        print('开流成功时长', different_time)

                        # 时间差保留 3位 毫秒
                        different_time_str = str(different_time)[:-3]
                        print(different_time_str)

                        # 将 点击屏幕时间 保存到Excel中.
                        colume_to_add_success = ['B']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', click_time,
                                                                colume_to_add_success)

                        # 将 开流成功的最后时间,保存到Excel中.
                        colume_to_add_success = ['C']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', success_live_play_time,
                                                                colume_to_add_success)

                        # 将 点击屏幕开流的次数 保存到Excel中.
                        colume_to_add_success = ['O']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)
                        # 将 开流成功 的 次数,保存到Excel中.
                        colume_to_add_success = ['P']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)

                        assert '当前设备开流成功' == '当前设备开流成功', " 当前设备开流成功。"
                        print("开流成功")

                        break
                    else:
                        continue

                else:
                    # 如果 最后一张截图,左上角仍没有事件戳,即判断为失败.
                    if jj == len(Screenshot_path_and_time_list):

                        # 将 最后一张截图上传到 HTML 报告中.
                        allure.attach.file(start_image_save_path, name="%s_start_flow_finally_%s" % (jj, start_flow),
                                           attachment_type=allure.attachment_type.JPG)
                        master.implicitly_wait(10)

                        # 将 点击屏幕时间 保存到Excel中.
                        colume_to_add_success = ['B']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', click_time,
                                                                colume_to_add_success)

                        # 将 开流失败的最后时间,保存到Excel中.
                        colume_to_add_success = ['C']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', '开流失败',
                                                                colume_to_add_success)

                        # 将 点击屏幕开流的次数 保存到Excel中.
                        colume_to_add_success = ['O']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)
                        # 将 开流成功/失败的 次数,保存到Excel中.
                        colume_to_add_success = ['P']
                        gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 0,
                                                                colume_to_add_success)

                        with allure.step('step3-1: 冷启app。step时间点：%s'
                                         % datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3]):

                            master.implicitly_wait(10)

                            # 终止应用程序 app
                            # master.terminate_app(app_id=android_package_name, timeout=10000)
                            # master.implicitly_wait(10)
                            # print(1)

                            # 杀死 App ,结束 App 进程
                            gz_public.kill_app_process(devices_name, android_package_name)
                            time.sleep(2)

                            # 关闭状态的APP，app_state=1 ,  0：应用未安装 , 1：应用已安装单未运行,  3：应用在后台运行 , 4：应用在前台运行
                            status = master.query_app_state(android_package_name)
                            print('关闭状态的APP，app_state=1, 实际状态:', status)

                            assert master.current_package != android_package_name

                            master.implicitly_wait(10)

                        print("开流失败,最后一张没有找到 时间戳")

                        # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
                        assert '当前设备开流成功' == '当前设备开流失败', " 当前设备开流成功。"

                    else:
                        continue

                jj += 1

            #
            #
            # WebDriverWait(master, timeout=45, poll_frequency=0.5).until(
            #     lambda x: x.find_element(AppiumBy.ID, 'com.huiyun.care.viewerpro:id/vertical_land_network_speed'))
            #
            # # 获取当前时间
            # live_play_time = datetime.now()
            # print(live_play_time)
            # master.implicitly_wait(10)
            # # 开流用时 小数点后 保留3位小数 毫秒级别
            # different_time = live_play_time - click_time
            # print(different_time)
            # different_time_str = str(live_play_time - click_time)[:-3]
            # print(different_time_str)
            #
            # # 截一张图
            # start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            # master.save_screenshot('./report/Ring/start_flow_%s.png' % start_flow)
            # time.sleep(3)
            #
            # # 将截图添加到报告中
            # allure.attach.file("./report/Ring/start_flow_%s.png" % start_flow, name="start flow",
            #                    attachment_type=allure.attachment_type.JPG)
            # master.implicitly_wait(10)
            #
            # # 确认进入了指定设备的开流页面，页面title应为设备名称
            # assert master.find_element(AppiumBy.ID,
            #                            'com.huiyun.care.viewerpro:id/double_screen_camera_name').text == dev_name
            #
            # # 判断 当前设备 开流成功 (开流页右上角 WiFi 和 顶部中间数据传输速度 两个icon 都出现,标志开流成功)
            # if gz_public.isElementPresent(driver=master, by="id",
            #                               value="com.huiyun.care.viewerpro:id/wifi_signal_iv") is True and gz_public.isElementPresent(
            #     driver=master, by="id",
            #     value="com.huiyun.care.viewerpro:id/vertical_land_network_speed") is True:
            #     # 将 点击屏幕时间 保存到Excel中.
            #     colume_to_add_success = ['B']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', click_time,
            #                                             colume_to_add_success)
            #
            #     # 将 开流成功的最后时间,保存到Excel中.
            #     colume_to_add_success = ['C']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', live_play_time,
            #                                             colume_to_add_success)
            #
            #     # 将 点击屏幕开流的次数 保存到Excel中.
            #     colume_to_add_success = ['O']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
            #                                             colume_to_add_success)
            #     # 将 开流成功/失败的 次数,保存到Excel中.
            #     colume_to_add_success = ['P']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
            #                                             colume_to_add_success)
            #
            #     assert '当前设备开流成功' == '当前设备开流成功', " 当前设备开流成功。"
            #
            # else:
            #     # 将 点击屏幕时间 保存到Excel中.
            #     colume_to_add_success = ['B']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', click_time,
            #                                             colume_to_add_success)
            #
            #     # 将 开流失败的最后时间,保存到Excel中.
            #     colume_to_add_success = ['C']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', '开流失败',
            #                                             colume_to_add_success)
            #
            #     # 将 点击屏幕开流的次数 保存到Excel中.
            #     colume_to_add_success = ['O']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 1,
            #                                             colume_to_add_success)
            #     # 将 开流成功/失败的 次数,保存到Excel中.
            #     colume_to_add_success = ['P']
            #     gz_public.result_save_excel_column_list('Ring_result.xlsx', 'Sheet1', 0,
            #                                             colume_to_add_success)
            #
            #     with allure.step('step3-1: 冷启app。step时间点：%s'
            #                      % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            #         # appium 1.22.2的用方法
            #         # master.close_app()
            #         master.terminate_app(android_package_name)
            #         master.implicitly_wait(10)
            #
            #     # 断言失败,用来结束本条用例后面的步骤,去执行下一条用例
            #     assert '当前设备开流成功' == '当前设备开流失败', " 当前设备开流成功。"
            #
            # '''
            # # 当开流不成功,屏幕出现刷新重试时,点击刷新重试按钮.
            # while gz_public.isElementPresent(driver=master, by="xpath",
            #                                  value='//android.widget.TextView[@text="%s"]' % '设备连接失败，请点击重试') is True:
            #     master.implicitly_wait(10)
            #     # 点击屏幕刷新重试按钮.
            #     master.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="%s"]' % '设备连接失败，请点击重试').click()
            #     time.sleep(40)
            #
            #     # 截一张图
            #     start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            #     master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
            #     time.sleep(3)
            #
            #     # 将截图添加到报告中
            #     allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
            #                        attachment_type=allure.attachment_type.JPG)
            #     master.implicitly_wait(10)
            #     break
            # '''
        #
        # with allure.step('step4：点击页面左上角的 返回，结束开流。step时间点：%s 。'
        #                  % (datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3])):
        #
        #     # 点击左上角的 返回按钮
        #     # master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
        #     # master.implicitly_wait(10)
        #     initPhone.keyEventSend(4)
        #     master.implicitly_wait(10)
        #
        #     # 确认回到了首页
        #     assert master.find_element(AppiumBy.ID, "com.huiyun.care.viewerpro:id/logo")

        with allure.step('step4: 冷启app。step时间点：%s'
                         % datetime.now().strftime("%Y-%m-%d_%H,%M,%S.%f")[:-3]):

            # 终止应用程序 app
            # master.terminate_app(app_id=android_package_name, timeout=10000)
            # master.implicitly_wait(10)
            # print(1)

            # 杀死 App ,结束 App 进程
            gz_public.kill_app_process(devices_name, android_package_name)
            time.sleep(2)

            # 关闭状态的APP，app_state=1 ,  0：应用未安装 , 1：应用已安装单未运行,  3：应用在后台运行 , 4：应用在前台运行
            status = master.query_app_state(android_package_name)
            print('关闭状态的APP，app_state=1, 实际状态:', status)

            assert master.current_package != android_package_name

            master.implicitly_wait(10)

    @allure.title('panda 开流')
    @allure.story('循环测试 摄像机 正常开流')
    def test_panda_live_play(self):
        self.test_public_open_flow_result('panda')

    @allure.title('ring 开流')
    @allure.story('循环测试 摄像机 正常开流')
    def test_ring_live_play(self):
        self.test_public_open_flow_result('ring')


if __name__ == '__main__':
    # V8P 长时间开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 20, "test_gzAndroidAuto.py::TestOpenFlow"
    #                                                    "::test_v8p_disconnect_flow_after_30_minutes",
    #              "--alluredir=./report/V8P"])

    # ring 多次开流
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_Huiyun_live_play.py::TestOpenFlow::test_panda_live_play",
                 "--alluredir=./report/Ring"])
