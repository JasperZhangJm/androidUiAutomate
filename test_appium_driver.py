from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from gz_public import get_dsc
from gz_start_appium import StartAppium
import time
import gz_public
import initPhone
from appium.webdriver.common.touch_action import TouchAction

devices = ['Galaxy S10e', 'moto g', 'SamsungA51', 'moto_z4']

dev_tmp = []

android_package_name = 'com.glazero.android'

for device in devices:
    tmp = get_dsc(device=device)
    dev_tmp.append(tmp)

phone_1 = dev_tmp.pop(0)
print('phone_1: ', phone_1)
phone_2 = dev_tmp.pop(0)
print('phone_2: ', phone_2)

StartAppium.start_appium(port=phone_1["port"])
time.sleep(3)
master = webdriver.Remote("http://127.0.0.1:%s" % phone_1["port"], phone_1["des"])

# 如果出现了引导蒙层，点击 知道了
while gz_public.isElementPresent(driver=master, by="id",
                                 value="com.glazero.android:id/btn_live_play_guide_next") is True:
    master.find_element(AppiumBy.ID, "com.glazero.android:id/btn_live_play_guide_next").click()
    master.implicitly_wait(10)
