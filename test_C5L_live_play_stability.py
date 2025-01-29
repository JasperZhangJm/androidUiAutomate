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

import datetime_self
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
import pyautogui

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['Pixel 7', 'Samsung S8', 'moto g', 'Pixel 7', 'SamsungSCV36', 'SamsungA51', 'moto_z4']

dev_tmp = []
# 慧云通讯 App 包名
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
    # master = webdriver.Remote("http://127.0.0.1:%s/wd/hub" % phone_1["port"], phone_1["des"])
    master = webdriver.Remote("http://127.0.0.1:%s" % phone_1["port"], phone_1["des"])

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
            time.sleep(3)

        # 在首页的话下滑刷新一下设备列表
        if gz_public.isElementPresent(driver=master, by="id", value="com.huiyun.care.viewerpro:id/logo") is True:
            gz_public.swipe_down(driver=master)
            # 等待下来刷新完成
            time.sleep(3)

        # 其他弹窗检测
        '''
        首页的其他弹窗如果影响测试需要在这添加，添加后跟每个方法执行完成后回到首页检查的弹窗相对应
        '''

    @allure.title('设备 开流30分钟后自动断流')
    @allure.story('用户使用设备开流30分钟后自动断流')
    def test_public_disconnect_flow_after_30_minutes(self, dev_model):
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
        master.implicitly_wait(20)
        # 获取 当前设备的 设备名
        dev_name = master.find_element(AppiumBy.ID, 'com.glazero.android:id/device_name').text
        # 获取设备的名字
        print("找到的设备名称是：%s，设备型号是：%s" % (dev_name, dev_model))

        with allure.step('step1: 在设备列表中滑动找到要开流的设备，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            # 确认找到了设备
            assert master.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("%s"))' % dev_name)
            master.implicitly_wait(20)

            # 确认找到了设备
            # 这样写有问题，如果页面中有多个设备，目标设备在下方，该方法会找上面的设备的对应的控件名字，所以不能这样写
            # assert master.find_element_by_id('com.glazero.android:id/device_name').text == dev_name

        with allure.step('step2: 点击前面拿到的设备屏幕,开始开流，例如，%s。step时间点：%s'
                         % (dev_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/device_name').click()

            # 获取当前时间
            click_time = datetime.now()
            print(click_time)
            master.implicitly_wait(20)

            # 确认进入了指定设备的开流页面，页面title应为设备名称
            assert master.find_element(AppiumBy.ID,
                                       'com.glazero.android:id/tv_title').text == dev_name

        with allure.step('step3: 开流开始后，开流时长 30分钟, 每 10秒 检查一次开流状态'):
            # 等待状态包括：正在建立访问通道...   正在连接网络服务...   实时视频加载中...   这些状态的id相同，如下：
            # 这些状态消失后，才成功开流
            # while gz_public.isElementPresent(driver=master, by="id",
            #                                  value="com.glazero.android:id/btn_full_screen") is True:
            #     time.sleep(1)
            #     break

            # 等待加载过程消失，mqtt、awake、p2p每个阶段超时时间是15秒，如果最后开流失败整个过程一共是45秒
            WebDriverWait(master, timeout=45, poll_frequency=2).until_not(
                lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))
            time.sleep(1)
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

                if gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/btn_full_screen") is True:

                    with allure.step('step6: 冷启app。step时间点：%s'
                                     % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                        # appium 1.22.2的用方法
                        # master.close_app()
                        master.implicitly_wait(10)
                        master.terminate_app(android_package_name)  # 查下 pid 是否存在.
                        master.implicitly_wait(10)

                    assert '预期开流成功' == '实际开流失败'
                    time.sleep(1)
            '''
            # 成功开流后记录开始的时间戳
            start_connect_flow_ts = datetime.now()
            print("开始开流时间是：", start_connect_flow_ts)

            # 开流开始后 截一张图
            start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            image_save_path = './report/C5L/start_flow_%s.png' % start_flow
            master.save_screenshot(image_save_path)
            time.sleep(3)

            # 将截图添加到报告中
            allure.attach.file("./report/C5L/start_flow_%s.png" % start_flow, name="start_flow_%s" % start_flow,
                               attachment_type=allure.attachment_type.JPG)
            master.implicitly_wait(10)

            # 声明一个变量:last_extracted_text_datetime 上一次截图 左上角时间为空 ,用于 if里 两次截图左上角时间的计算
            last_extracted_text_datetime = None
            # 声明一个变量:last_connect_flow_ts 上一次截图时的时间戳为空 ,用于 if里 两次截图时,时间戳的计算
            last_connect_flow_ts = None

            # 前 30分钟每 10 秒检查一次开流状态，10*6*30 = 1800秒，即 30分钟,共180次,下面 for循环 1 次,截图执行2次,所以 循环 90次 即可,填 (1,91).
            for ii in range(1, 181):
                try:
                    print("当前是第%s次" % ii)
                    # 截图时间
                    connect_flow_ts = datetime.now()
                    print("截图时间是：", connect_flow_ts)
                    # # 当前时间 加上 1 秒,用于 if 判断中 与本次截图中 文本时间戳 对比,比文本时间戳大,说明出现了卡顿
                    # connect_flow_ts_datetime = connect_flow_ts - datetime.timedelta(seconds=1)
                    # print("截图时间是：", connect_flow_ts_datetime)

                    # 开流开始后 截一张图
                    start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    start_image_save_path = './report/C5L/%s_start_flow_%s.png' % (ii, start_flow)
                    master.save_screenshot(start_image_save_path)

                    # img = pyautogui.screenshot(region=[0, 0, 100, 100])  # x,y,w,h
                    # # img.save('screenshot.png')
                    # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

                    # 将截图添加到报告中
                    allure.attach.file("./report/C5L/%s_start_flow_%s.png" % (ii, start_flow),
                                       name="%s_start_flow_%s" % (ii, start_flow),
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)

                    # 提取开流页面,左上角的时间戳.
                    # 将 本次开流截图,转成黑白色,并且保存到 路径  image_black_and_white_path_name  中
                    image_black_and_white_path_name = './report/C5L/%s_start_flow_%s.png' % (ii, start_flow)
                    # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中
                    image_partial_path_name = './report/C5L/%s-1_start_flow_%s.png' % (ii, start_flow)
                    # 将 本次开流截图,转成黑白色,并且保存到 路径  image_black_and_white_path_name  中
                    gz_public.picture_contrast_black_and_white(start_image_save_path,
                                                               image_black_and_white_path_name)
                    # 将 黑白截图 再节选出 需要的部分,保存到路径 image_partial_path_name 中,并且识别 其中的文字 传给start_extracted_text
                    start_extracted_text = gz_public.get_image_text_simple(image_black_and_white_path_name, 0, 600, 250,
                                                                           1080, 300, image_partial_path_name)

                    print(start_extracted_text)  # 例: dan.08.2024 20:18:27
                    # 获取 提取到的字符串中的  时间.
                    start_extracted_text_time = start_extracted_text.split(' ')[1]
                    print('左上角时间戳字符串', start_extracted_text_time)  # 例: 20:18:27

                    # 将 识别到的时间转化成 datetime 类型
                    start_extracted_text_datetime = gz_public.time_format_conversion_datetime_format(
                        start_extracted_text_time)
                    print('将 左上角时间戳转化成时间格式:', start_extracted_text_datetime)

                    # 强制等待 6 秒
                    # time.sleep(8)

                    '''
                    # 截图时间
                    connect_flow_ts = datetime.now()
                    print("截图时间是：", connect_flow_ts)
    
                    # 开流开始后 截下一张图
                    next_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    next_image_save_path = './report/C5L/%s_start_flow_%s.png' % (ii, next_flow)
                    master.save_screenshot(next_image_save_path)
    
                    # 将截图添加到报告中
                    allure.attach.file("./report/C5L/%s_start_flow_%s.png" % (ii, next_flow),
                                       name="%s_start_flow_%s" % (ii, next_flow),
                                       attachment_type=allure.attachment_type.JPG)
                    master.implicitly_wait(10)
    
                    # 提取下一次 开流页面,左上角的时间戳.
                    picture_contrast_path_name = './report/C5L/%s_start_flow_%s.png' % (ii, next_flow)
                    gz_public.picture_contrast_black_and_white(start_image_save_path, picture_contrast_path_name)
                    # 取出 要识别的部分  截图并识别
                    next_extracted_text = gz_public.get_image_text_simple(picture_contrast_path_name, 0, 600, 200, 1080,
                                                                           250)
                    print(next_extracted_text)
                    connect_flow_ts = datetime.now()
                    print("完成提取图片时间戳时间是：", connect_flow_ts)
                    master.implicitly_wait(10)
                    
    
                    # 将 两次截图的时间,记录到 Excel 上
                    content_full_list_to_add = [start_extracted_text, next_extracted_text]
                    column_full_list_to_add = ['B', 'C']
                    gz_public.result_save_excel_full_list('./C5L_result.xlsx', 'Sheet1', content_full_list_to_add,
                                                          column_full_list_to_add)
                    time.sleep(6)
                    '''

                    content_full_list_to_add = [connect_flow_ts, start_extracted_text_datetime]
                    column_full_list_to_add = ['B', 'C']
                    gz_public.result_save_excel_full_list('./C5L_result.xlsx', 'Sheet1', content_full_list_to_add,
                                                          column_full_list_to_add)

                    if ii == 1:
                        # 当 第一次执行 for循环,截图识别时间戳文字,由于没有 上一次截图 的对比,所以直接判断 通过.
                        # 执行次数
                        colume_to_add_success = ['L']
                        gz_public.result_save_excel_column_list('C5L_result.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)
                        master.implicitly_wait(10)

                        # 将 执行失败 次数,统计在Excel中.
                        column_full_list_to_add = ['M', 'N']
                        gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 1,
                                                                column_full_list_to_add)
                        master.implicitly_wait(10)

                        # 将 执行失败 结果,统计在Excel中.
                        column_full_list_to_add = ['E']
                        gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 'pass',
                                                                column_full_list_to_add)

                        # 本次 截图时的时间戳 传递给 下一次循环,用于时间对比,判断当前由于卡顿.
                        last_connect_flow_ts = connect_flow_ts
                        print('上次截图时,时间戳', last_connect_flow_ts)

                        # 本次 截图识别的时间戳 传递给 下一次循环,用于时间戳内容对比,判断当前由于卡顿.
                        last_extracted_text_datetime = start_extracted_text_datetime
                        print('上次截图左上角时间戳', last_extracted_text_datetime)

                        print('没有出现卡顿')

                        time.sleep(8)

                        master.implicitly_wait(10)

                    else:
                        # 计算 两次截图时间戳差值,参与下面 if 判断的对比.
                        different_connect_flow_ts = connect_flow_ts - last_connect_flow_ts
                        print('两次截图当时,时间戳差值: %s ,本次: %s ,上次: %s ' % (different_connect_flow_ts,
                              connect_flow_ts, last_connect_flow_ts))

                        # 计算 两次截图左上角的时间戳差值,参与下面 if 判断的对比.
                        different_extracted_text_datetime = start_extracted_text_datetime - last_extracted_text_datetime
                        print('两次截图左上角的时间戳差值: %s ,本次: %s ,上次: %s ' % (different_extracted_text_datetime,
                              start_extracted_text_datetime, last_extracted_text_datetime))

                        connect_flow_ts = datetime.now()
                        print("完成提取图片时间戳时间是：", connect_flow_ts)

                        # 如果 两次当前截图时间差值 <= 两次截图左上角时间戳值 + 2 秒,即判断为 出现卡顿
                        if different_connect_flow_ts <= different_extracted_text_datetime + datetime_self.timedelta(
                                seconds=2):
                            # 执行次数
                            colume_to_add_success = ['L']
                            gz_public.result_save_excel_column_list('C5L_result.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            master.implicitly_wait(10)

                            # 将 执行成功 次数,统计在Excel中.
                            column_full_list_to_add = ['M', 'N']
                            gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 1,
                                                                    column_full_list_to_add)
                            master.implicitly_wait(10)

                            # 将 执行成功 结果,统计在Excel中.
                            column_full_list_to_add = ['E']
                            gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 'pass',
                                                                    column_full_list_to_add)

                            # 本次 截图时的时间戳 传递给 下一次循环,用于时间对比,判断当前由于卡顿.
                            last_connect_flow_ts = connect_flow_ts
                            print('上次截图时,时间戳', last_connect_flow_ts)

                            # 本次 截图识别的时间戳 传递给 下一次循环,用于时间戳内容对比,判断当前由于卡顿.
                            last_extracted_text_datetime = start_extracted_text_datetime
                            print('上次截图左上角时间戳', last_extracted_text_datetime)

                            print('没有出现卡顿')

                            time.sleep(8)

                            master.implicitly_wait(10)

                            assert different_connect_flow_ts <= different_extracted_text_datetime + datetime_self.timedelta(
                                seconds=2), "上次截图时,时间戳: %s ,本次截图时,时间戳: %s ,上次左上角时间戳 %s ,本次左上角时间戳: %s ,如果 2-1 <= 4-3 +2秒 ,表示没有出现卡顿" % (
                                connect_flow_ts, last_connect_flow_ts, start_extracted_text_datetime,
                                last_extracted_text_datetime)
                            master.implicitly_wait(10)

                        else:
                            # 执行次数
                            colume_to_add_success = ['L']
                            gz_public.result_save_excel_column_list('C5L_result.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            master.implicitly_wait(10)

                            # 将 执行失败 次数,统计在Excel中.
                            column_full_list_to_add = ['M', 'N']
                            gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 0,
                                                                    column_full_list_to_add)
                            master.implicitly_wait(10)

                            # 将 执行失败 结果,统计在Excel中.
                            column_full_list_to_add = ['E']
                            gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 'fail',
                                                                    column_full_list_to_add)

                            # 本次 截图时的时间戳 传递给 下一次循环,用于时间对比,判断当前由于卡顿.
                            last_connect_flow_ts = connect_flow_ts
                            print('上次截图时,时间戳', last_connect_flow_ts)

                            # 本次 截图识别的时间戳 传递给 下一次循环,用于时间戳内容对比,判断当前由于卡顿.
                            last_extracted_text_datetime = start_extracted_text_datetime
                            print('上次截图左上角时间戳', last_extracted_text_datetime)

                            print('出现卡顿')

                            master.implicitly_wait(10)
                            '''
                            with allure.step('step3-1: 冷启app。step时间点：%s'
                                             % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
                                # appium 1.22.2的用方法
                                # master.close_app()
                                master.implicitly_wait(10)
                                master.terminate_app(android_package_name)  # 查下 pid 是否存在.
                                master.implicitly_wait(10)
                            '''

                            try:
                                assert different_connect_flow_ts <= different_extracted_text_datetime + datetime_self.timedelta(
                                    seconds=2), "上次截图时,时间戳: %s ,本次截图时,时间戳: %s ,上次左上角时间戳 %s ,本次左上角时间戳: %s ,如果 2-1 <= 4-3 +2秒 ,表示没有出现卡顿" % (
                                    connect_flow_ts, last_connect_flow_ts, start_extracted_text_datetime,
                                    last_extracted_text_datetime)
                            except:
                                time.sleep(8)
                                continue
                except:
                    # 当开流不成功,屏幕出现刷新重试时,点击刷新重试按钮.
                    while gz_public.isElementPresent(driver=master, by="id",
                                                     value="com.glazero.android:id/bt_play_retry") is True:
                        master.implicitly_wait(10)
                        # 点击屏幕刷新重试按钮.
                        master.find_element(AppiumBy.XPATH,
                                            '//android.widget.TextView[@text="%s"]' % '刷新重试').click()

                        # 截一张图
                        start_flow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                        master.save_screenshot('./report/C6L/start_flow_%s.png' % start_flow)
                        master.implicitly_wait(10)

                        # 将截图添加到报告中
                        allure.attach.file("./report/C6L/start_flow_%s.png" % start_flow, name="start flow",
                                           attachment_type=allure.attachment_type.JPG)
                        master.implicitly_wait(10)

                        time.sleep(15)

                        # 执行次数
                        colume_to_add_success = ['L']
                        gz_public.result_save_excel_column_list('C5L_result.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)
                        master.implicitly_wait(10)

                        # 将 执行失败 次数,统计在Excel中.
                        column_full_list_to_add = ['M', 'N']
                        gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 0,
                                                                column_full_list_to_add)
                        master.implicitly_wait(10)

                        # 将 执行失败 结果,统计在Excel中.
                        column_full_list_to_add = ['E']
                        gz_public.result_save_excel_column_list('./C5L_result.xlsx', 'Sheet1', 'fail',
                                                                column_full_list_to_add)
                        master.implicitly_wait(10)

                        time.sleep(8)

                        continue

                    # 本次 截图时的时间戳 传递给 下一次循环,用于时间对比,判断当前由于卡顿.
                    last_connect_flow_ts = connect_flow_ts
                    print('上次截图时,时间戳', last_connect_flow_ts)

                    # 本次 截图识别的时间戳 传递给 下一次循环,用于时间戳内容对比,判断当前由于卡顿.
                    last_extracted_text_datetime = start_extracted_text_datetime
                    print('上次截图左上角时间戳', last_extracted_text_datetime)

                    print('出现卡顿')

                    time.sleep(8)
                    # time.sleep(6)

                ii = ii + 1

            end_connect_flow_ts = datetime.now()
            print("执行完成 时间是：", end_connect_flow_ts)
            master.implicitly_wait(10)

        with allure.step('step4：校验断流的时间点距离开流的时间点间隔是30分钟即1800秒'):
            with allure.step('step4-1：开流时间点为：%s' % start_connect_flow_ts):
                print(start_connect_flow_ts)
                pass
            with allure.step('step4-2：断流时间点为：%s' % end_connect_flow_ts):
                print(end_connect_flow_ts)
                pass
                # 在step3和step4中已经获得了 开流时间点和断流时间点，计算差值
                different_time_str = str(end_connect_flow_ts - start_connect_flow_ts)[:-3]
                print(different_time_str)
            with allure.step('step4-3：开流到断流时间差为：%s' % different_time_str):
                print(different_time_str)
                pass

            #     # 在step3和step4中已经获得了 开流时间点和断流时间点，计算差值
            #     result = int(disconnect_flow_ts - connect_flow_ts)
            #     print("断流时间点和开流时间点差值是：", result)
            #     res_sec = result // 1000
            #     print("开流时长是：%d秒" % res_sec)
            # with allure.step('step5-3：断流时间点和开流时间点差值是：%d秒' % res_sec):
            #     # 断言误差在10秒之内，程序运行时间，例如，截图、保存、allure处理附件等，实际看误差有：1秒，2秒、3秒
            #     assert (res_sec - 1800) <= 10, "实际开流时间大于1810秒"

        with allure.step('step5：点击页面左上角的 返回，结束开流。step时间点：%s 。开流到断流的时间差: %s '
                         % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), different_time_str)):
            # 点击左上角的 返回按钮
            # master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            # master.implicitly_wait(10)
            initPhone.keyEventSend(4)
            master.implicitly_wait(10)

            # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")

        with allure.step('step6: 冷启app。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # appium 1.22.2的用方法
            # master.close_app()
            master.implicitly_wait(10)
            master.terminate_app(android_package_name)
            master.implicitly_wait(10)

    @allure.title('C2E 设备开流30分钟后,自动断流')
    @allure.story('用户使用设备开流30分钟后,自动断流')
    def test_c2e_live_play(self):
        self.test_public_disconnect_flow_after_30_minutes('C2E')

    @allure.title('C5L设备开流30分钟后,自动断流')
    @allure.story('用户使用设备开流30分钟后,自动断流')
    def test_c5l_live_play(self):
        self.test_public_disconnect_flow_after_30_minutes('C5L')


if __name__ == '__main__':
    # V8P 长时间开流
    # pytest.main(["-q", "-s", "-ra", "--count=%d" % 20, "test_gzAndroidAuto.py::TestOpenFlow"
    #                                                    "::test_v8p_disconnect_flow_after_30_minutes",
    #              "--alluredir=./report/V8P"])

    # ring 多次开流
    pytest.main(
        ["-q", "-s", "-ra", "--count=%d" % 10, "test_C5L_live_play_stability.py::TestOpenFlow::test_c2e_live_play",
         "--alluredir=./report/C5L"])
