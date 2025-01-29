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
import datetime
import re

logging.basicConfig(filename='./log/runTest.log', level=logging.DEBUG, datefmt='[%Y-%m-%d %H:%M:%S]',
                    format='%(asctime)s %(levelname)s %(filename)s [%(lineno)d] %(threadName)s : %(message)s')

devices = ['Samsung S8', 'moto g', 'SamsungSCV36', 'SamsungA51', 'moto_z4']

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


@allure.feature("push专项")
class TestPush(object):

    @staticmethod
    def setup_class():
        # # 获取完成后清除logcat
        r_obj = os.popen("adb logcat -c")
        r_obj.close()

    def test_public_push(self, dev_model):
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
        # dev_name = gz_public.get_device_name(model=dev_model)
        # print("找到的设备名称是：%s，设备型号是：%s" % (dev_name, dev_model))
        with allure.step(
                'step1: 进入手机首页,打开通知栏。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 进入手机首页
            initPhone.keyEventSend(3)
            # 打开通知栏
            master.open_notifications()
            time.sleep(1)

        with allure.step(
                'step2: 点击通知栏中最新一条Aosu通知。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                    time.localtime())):
            # 展开 Aosu所有的 push通知：找到通知栏中Aosu图标并点击。
            master.implicitly_wait(10)
            master.find_elements(AppiumBy.ID, 'android:id/app_name_text')[0].click()
            time.sleep(1)

            # 截一张图
            start_push = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/C6L/start_flow_%s.png' % start_push)

            # 将截图添加到报告中
            allure.attach.file("./report/C6L/start_flow_%s.png" % start_push, name="start push",
                               attachment_type=allure.attachment_type.JPG)

            # 点击最近的一个 push 通知 进行跳转。
            master.find_elements(AppiumBy.ID, 'android:id/title')[0].click()
            # 记录一次执行测试,保存再Excel中,AL列
            colume_to_add_success = ['AL']
            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                    colume_to_add_success)
        with allure.step(
                'step3: 跳转成功后,判断视频处于正在播放状态。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                           time.localtime())):
            master.implicitly_wait(40)
            '''

            # 当跳转后  网络错误页  出现时,点击 刷新按钮.
            while gz_public.isElementPresent(driver=master, by="id",
                                             value="com.glazero.android:id/tip") is True:
                master.find_element(AppiumBy.ID, 'com.glazero.android:id/refresh').click()
                master.implicitly_wait(10)
                
            '''

            # 展开 Aosu所有的 push通知：找到通知栏中Aosu图标并点击。
            # print('1')
            # WebDriverWait(master, timeout=15, poll_frequency=2).until_not(
            #     lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/pb_progress_bar'))
            # print('2')
            # 展开 Aosu所有的 push通知：找到通知栏中Aosu图标并点击。
            # WebDriverWait(master, timeout=20, poll_frequency=2).until_not(
            #     lambda x: x.find_element(AppiumBy.ID, 'com.glazero.android:id/tv_live_play_loading'))

            # 点击一下屏幕 播放器的上面:com.glazero.android:id/view_title
            # master.find_element(AppiumBy.ID, 'com.glazero.android:id/view_title').click()

            # master.implicitly_wait(10)
            # 点击一下屏幕暂停按钮.
            master.find_element(AppiumBy.ID, 'com.glazero.android:id/img_play').click()

            # 截一张图
            push_skip = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            master.save_screenshot('./report/C6L/start_flow_%s.png' % push_skip)

            # 将截图添加到报告中
            allure.attach.file("./report/C6L/start_flow_%s.png" % push_skip, name="push skip",
                               attachment_type=allure.attachment_type.JPG)
            # 记录一次执行测试,保存再Excel中,AM列
            colume_to_add_success = ['AM']
            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                    colume_to_add_success)

            # 播放按钮存在,即为跳转到回放成功.
            if gz_public.isElementPresent(driver=master, by="id",
                                          value="com.glazero.android:id/img_play") is True:
                print('进入卡录页面,视频播放正常')
                with allure.step(
                        'step3-1: 判断当前播放器事件,处于播放状态。step时间点：%s' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                 time.localtime())):
                    # 播放器的视频,正在处于:播放状态：startPlaybackInternal start onSuccess   暂停状态：pausePlayBack onSuccess
                    player_video_event_start_time = gz_public.select_log_keyword_state_medium(
                        '获取播放器当前播放状态 正在播放', 'TyPreviewCenter', 'startPlaybackInternal',
                        'onSuccess', -1)
                    print(player_video_event_start_time)

                with allure.step(
                        'step3-2: 从跳转的push通知中,获取事件事件时间 和 该事件设备的SN 。step时间点：%s' % time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime())):
                    # 从跳转的 push通知,获取事件开始时间
                    # 开始时间：eventTime=   push通知 时间：pushTime=
                    push_video_event_start_time_str = gz_public.select_log_keyword_state_medium(
                        '从跳转的push通知中,获取事件开始时间 和 该事件设备的SN ', 'GzPush',
                        'clearIntent intentMessage=', 'eventTime=', -1)
                    print(push_video_event_start_time_str)
                    if len(push_video_event_start_time_str) == 0:
                        print("push中事件 开始时间 为空")
                        # 再手机中 查找当时时间的log日志,并上传到 allure的 HTML报告中.
                        gz_public.log_upload_html('Push_C9L')
                        master.implicitly_wait(10)
                        assert push_video_event_start_time_str == 'push中事件 开始时间 为空', "push中事件 开始时间 为空。"
                    else:
                        get_push_video_event_start_time_str = push_video_event_start_time_str.split("=")[1]
                        get_push_video_event_start_time_str = get_push_video_event_start_time_str.split(",")[0]
                        print('push中事件 开始时间 ', get_push_video_event_start_time_str)
                        # 将 事件时间 字符串格式转化成 datetime时间格式时间戳
                        push_video_event_start_time = gz_public.time_format_conversion_datetime_format(
                            get_push_video_event_start_time_str)
                        print(push_video_event_start_time)
                        master.implicitly_wait(10)

                        # 从跳转的 push通知,获取该事件 设备的 SN
                        # sn 字段 :  ,"sn":"",
                        push_video_event_dev_sn_str = gz_public.select_log_keyword_state_medium(
                            '从跳转的push通知中,获取该事件 设备的 SN ', 'GzPush', 'clearIntent intentMessage=', 'sn',
                            -1)
                        print(push_video_event_dev_sn_str)
                        if len(push_video_event_dev_sn_str) == 0:
                            print("push中事件 sn字符串 为空")
                            # 再手机中 查找当时时间的log日志,并上传到 allure的 HTML报告中.
                            gz_public.log_upload_html('Push_C9L')
                            master.implicitly_wait(10)
                            assert push_video_event_start_time_str == 'push中事件 sn字符串 为空', "push中事件 sn字符串 为空。"
                        else:
                            # 找到的 SN 是list类型
                            push_video_event_dev_sn_list = re.findall("(?<=\"sn\":\").*?(?=\",)", push_video_event_dev_sn_str) #  以某个字符开始、某个字符结束，期待的提取结果不包含首、末字符串： a = re.findall("(?<=开始字符串).*?(?=末字符串)",str) 或者 a = re.findall(".*开始字符串(.*)末字符串*",str)
                            print(push_video_event_dev_sn_list)
                            # 将找到的结果 list类型 转化成 字符串类型
                            get_push_video_event_dev_sn_str = str(push_video_event_dev_sn_list)
                            print(get_push_video_event_dev_sn_str)
                            # 取出 SN 值
                            push_video_event_dev_sn = get_push_video_event_dev_sn_str.split("\'")[1]
                            print("push中事件 sn字符串", push_video_event_dev_sn)
                            master.implicitly_wait(10)

                with allure.step(
                        'step3-3: 获取push通知跳转的位置。例如:卡录、云录、开流step时间点：%s' % time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime())):
                    # 获取 push通知 跳转的位置
                    push_jump_position = gz_public.select_log_keyword_state_medium('获取push通知跳转的位置',
                                                                                   'Playback_Companion',
                                                                                   'selectDefaultTab',
                                                                                   'storageType=', -1)
                    print(push_jump_position)
                    get_push_jump_position = push_jump_position.split("=")[1]

                with allure.step(
                        'step3-4: 判断从push跳转后，播放的事件是push的事件。step时间点：%s' % time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime())):
                    # 获取播放器当前播放事件的 设备SN
                    # 开始时间：startTimeSec=   结束时间：endTimeSec=
                    player_video_event_dev_sn = gz_public.select_log_keyword_state_medium(
                        '获取播放器当前播放事件的 设备SN ', 'TyPreviewCenter', 'startPlaybackInternal',
                        'sn=', -2)
                    print(player_video_event_dev_sn)
                    player_video_event_dev_sn = player_video_event_dev_sn.split("=")[1]
                    print('获取播放器当前播放事件的 设备SN: ', player_video_event_dev_sn)
                    print(type(player_video_event_dev_sn))
                    # 设备类型 取 SN 的前三位,
                    push_dev_model = player_video_event_dev_sn[:3]

                    # 获取播放器当前播放事件的 开始时间
                    # 开始时间：startTimeSec=   结束时间：endTimeSec=
                    player_video_event_start_time = gz_public.select_log_keyword_state_medium(
                        '获取播放器当前播放事件的 开始时间', 'TyPreviewCenter', 'startPlaybackInternal',
                        'startTimeSec=', -2)
                    print(player_video_event_start_time)
                    get_player_video_event_start_time = player_video_event_start_time.split("=")[1]
                    print('获取播放器当前播放事件的 开始时间', get_player_video_event_start_time)
                    print(type(get_player_video_event_start_time))

                    # 获取播放器当前播放事件的 结束时间
                    # 开始时间：startTimeSec=   结束时间：endTimeSec=
                    player_video_event_end_time = gz_public.select_log_keyword_state_medium(
                        '获取播放器当前播放事件的 结束时间', 'TyPreviewCenter', 'startPlaybackInternal',
                        'endTimeSec=', -2)
                    print(player_video_event_end_time)
                    get_player_video_event_end_time = player_video_event_end_time.split("=")[1]
                    print('获取播放器当前播放事件的 结束时间', get_player_video_event_end_time)
                    print(type(get_player_video_event_end_time))

                    # 将 录制预录开始时间的 字符串 转化成 时间戳  例如:1609459200
                    player_video_event_start_time_stamp = datetime.datetime.fromtimestamp(
                        int(get_player_video_event_start_time))
                    print('关键帧误差处理前,播放器当前播放事件的 开始时间', player_video_event_start_time_stamp)
                    print(type(player_video_event_start_time_stamp))

                    # 误差处理,播放器当前播放事件的 开始时间 减去 2秒,因为tuya找关键帧有误差,没找到时,前后浮动几秒去找关键帧
                    player_video_event_start_time = player_video_event_start_time_stamp - datetime.timedelta(seconds=3)
                    print('关键帧误差处理后,播放器当前播放事件的 开始时间', player_video_event_start_time)
                    print(type(player_video_event_start_time))

                    # 将 录制预录结束时间的 字符串 转化成 时间戳  例如:1609459200
                    player_video_event_end_time = datetime.datetime.fromtimestamp(int(get_player_video_event_end_time))
                    print('播放器当前播放事件的 结束时间', player_video_event_end_time)
                    print(type(player_video_event_end_time))

                    print('push 通知中 事件开始时间', push_video_event_start_time)

                    '''
                    # 获取 事件预录时间 : 事件时间 - 事件预录开始时间
                    different_time = gz_public.time_difference_simple(get_push_video_event_start_time, dt_obj)
                    

                    # 将 预录时间存储在 data1.xlsx 中
                    colume_to_add_success = ['AK']
                    gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                            colume_to_add_success)

                    colume_to_add_success = ['B']
                    gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', different_time,
                                                            colume_to_add_success)
                    # 将 时间类型转换成字符串类型,
                    str_event_prerecord_time = gz_public.datetime_timedelta_change_string(different_time)
                    print(type(str_event_prerecord_time))
                    event_prerecord_time_sec_millisecond = str_event_prerecord_time.split(":")[2]
                    event_prerecord_time_sec = event_prerecord_time_sec_millisecond.split(".")[0]
                    '''

                    # 如果预录时间  小于 10 秒  ,判断为:预录时间合理. int(player_video_event_start_time) < push_video_event_start_time < int(player_video_event_end_time)
                    if player_video_event_start_time <= push_video_event_start_time <= player_video_event_end_time:
                        print('视频预录制时间符合预期，push跳转后事件播放正确')
                        assert push_video_event_dev_sn == player_video_event_dev_sn
                        # 将不同型号设备 push通知跳转成功的次数 存储在Excel中
                        while push_dev_model == 'V8S':
                            # 将 V8S push 跳转成功的次数 存储在 AO 中
                            colume_to_add_success = ['AO']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C2E':
                            # 将 C2E push 跳转成功的次数 存储在 AP 中
                            colume_to_add_success = ['AP']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C5L':
                            # 将 C5L push 跳转成功的次数 存储在 AQ 中
                            colume_to_add_success = ['AQ']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C6L':
                            # 将 C5L push 跳转成功的次数 存储在 AR 中
                            colume_to_add_success = ['AR']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C9L':
                            # 将 C9S push 跳转成功的次数 存储在 AS 中
                            colume_to_add_success = ['AS']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C9E':
                            # 将 C9S push 跳转成功的次数 存储在 AT 中
                            colume_to_add_success = ['AT']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break

                        while push_dev_model == 'C9S':
                            # 将 C9S push 跳转成功的次数 存储在 AU 中
                            colume_to_add_success = ['AU']
                            gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                    colume_to_add_success)
                            break
                        # 将 push 跳转成功的次数 存储在 AN 中
                        colume_to_add_success = ['AN']
                        gz_public.result_save_excel_column_list('./data1.xlsx', 'Sheet1', 1,
                                                                colume_to_add_success)
                    else:
                        # 获取 当前 App和tuya日志,并上传到 HTML报告中
                        gz_public.log_upload_html('Push_C9L')
                        # 视频录制时间,不符合预期,该条用例执行失败,结束用例,执行下一条.
                        assert player_video_event_start_time <= push_video_event_start_time <= player_video_event_end_time, '回放中视频的开始时间（误差处理后）: %s；push中事件开始时间：%s ；回放视频结束时间：%s ；回放中视频的开始时间（误差处理前）：%s ' % (
                            player_video_event_start_time, push_video_event_start_time, player_video_event_end_time,
                            player_video_event_start_time_stamp)
            else:
                # 获取 当前 App和tuya日志,并上传到 HTML报告中
                gz_public.log_upload_html('Push_C9L')
                assert 0 == 1, "跳转后,展示失败。"

        with allure.step('step4：点击页面左上角的 返回Aosu首页，。step时间点：%s'
                         % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
            # 点击左上角的 返回按钮
            # master.find_element(AppiumBy.ID, 'com.glazero.android:id/btn_back').click()
            # master.implicitly_wait(10)
            initPhone.keyEventSend(4)
            master.implicitly_wait(10)

            # 确认回到了首页
            assert master.find_element(AppiumBy.ID, "com.glazero.android:id/img_tab_device")
            print('单条用例执行完成')
            # 按下home键 将App置后台
            initPhone.keyEventSend(3)
            time.sleep(180)

        # with allure.step('step5: 冷启app。step时间点：%s'
        #                  % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
        #     # appium 1.22.2的用方法
        #     # master.close_app()
        #     master.terminate_app(android_package_name)
        #     master.implicitly_wait(10)

    @allure.title('多次点击 push通知 并跳转 ')
    @allure.story('循环测试 正常收到 push，并正常跳转')
    def test_c9l_push(self):
        self.test_public_push('C9L')


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
    pytest.main(["-q", "-s", "-ra", "--count=%d" % 200, "test_push.py::TestPush::test_c9l_push",
                 "--alluredir=./report/Push_C9L"])
