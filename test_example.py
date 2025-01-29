import os
import re
import subprocess
import time
import gz_public
import initPhone
from signal import SIGTERM

# coding=utf-8
# tmp = gz.get_devices_list()
# print(rst.content.decode('utf-8'))
# print(rst)
# print(tmp)
# str = "中国 +86"
# region = list(str)
# print(region[3:-1])
# print(str[-3:])
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

def get_app_log(log_type, log_date, current_time, numbers_of_lines=1000):
    """
    获取app日志或者涂鸦日志
    :param current_time: 取日志时的时间，格式：年月日-时分秒，用于命名文件，不同的附件要对应不同的文件
    :param log_type: app 或者 ty
    :param log_date: 日志文件中的日期例如，20230510，用于选择对应的日志文件
    :param numbers_of_lines：返回日志的行数，默认是最新的1000行
    :结果: 将重定向的日志文件pull到本地，作为allure的attachment
    """
    if log_type == 'app':
        file_name = 'glazero_app_android_' + str(log_date) + '.log'
    elif log_type == 'ty':
        file_name = 'glazero_app_android_ty_' + str(log_date) + '.log'

    # 获取device id
    cmd = 'adb devices'
    with os.popen(cmd, 'r') as f_log:
        devs_id = f_log.readlines()
        dev_id = re.findall(r'^\w*\b', devs_id[1])[0]

    # 进入adb shell后进入日志目录，获取对应日期和对应日志类型的的日志
    cmd = 'adb -s %s shell "cd /sdcard/Android/data/com.glazero.android/files/log && ls && cat %s | tail -n %d > ' \
          '%s_log_%s.log && ls"' % (dev_id, file_name, numbers_of_lines, log_type, current_time)
    os.system(cmd)

    # 将到出的日志pull到本地
    cmd = 'adb pull /sdcard/Android/data/com.glazero.android/files/log/%s_log_%s.log ./report/V8P/log_attch' % (
        log_type, current_time)
    os.system(cmd)


def get_app_version_name():
    cmd = 'aapt dump badging ' + './resource/aosu_app_android_debug_1.11.18.5119_1683367354540.apk'
    with os.popen(cmd, 'r') as f_obj:
        lines = f_obj.readlines()
        app_version_name = re.findall(r'\d+\.\d+\.\d+\.[0-9]{4}', lines[0])[0]

    return app_version_name


'''


    try:
        with open(file_name, 'r', encoding='utf-8') as f_obj:
            lines = f_obj.readlines()
    except FileNotFoundError:
        print("没有找到日志文件" + str(log_date))
        return None
    else:
        last_n_lines = lines[-numbers_of_lines:]
        return last_n_lines


contents = get_app_log('app', current_time, 1000)

print(contents)
'''
# current_date = time.strftime("%Y%m%d", time.localtime())
# current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

# print(current_date)
# print(current_time)

# get_app_log('app', current_date, current_time, 500)
# get_app_log('ty', current_date, current_time, 300)
# ii = gz_public.get_user_type()
# print(ii)
# version = get_app_version_name()
# print(version)
# if '1.11.18.5119' in '1.11.18.5119 \
# 2023/05/06 18:04:30':
#     print('adsf')
# temp = gz_public.get_devices_list()
# print(temp)
# dev_name = []
# dev_sn = []
# for device in temp:
#     dev_name.append(device["name"])
#     dev_sn.append(device["sn"])

# print(len(dev_name))
# print(dev_sn)
'''
tmp1 = int(round(time.time() * 1000))
print(tmp1)

time.sleep(10)

tmp2 = int(round(time.time() * 1000))
print(tmp2)

result = int(tmp2 - tmp1)
print(result)
res_sec = result // 1000
print("开流时长是：%d秒" % res_sec)
# print("开流时长是：%d秒" % result//1000)
'''

# assert 0 == 1, "0不等于1，断言失败了！"

# res = initPhone.get_dev_play_state()
# print(res)
'''
cmd = 'adb -s R58N828LKMP shell logcat -v time -s LivePlayer \"\| grep -e playState && C6L2BA110000042\"'
print(cmd)
results = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)
results.terminate()
results.kill()

for line in results.stdout.readlines():
    print(line)

# 清除logcat
os.popen("adb logcat -c")
'''
#os.killpg(process.pid, SIGTERM)
'''
res = os.popen(cmd).read()
os.popen().closed
print(res)
'''
# res_ru = res.read()
# res.close()
'''
with os.popen(cmd, 'r') as f_obj:
    lines = f_obj.readlines()
    f_obj.close()
print(lines[0])
'''
# print(play_state)

