# coding=utf-8
__author__ = 'gucuijuan'
from config import *
from run_command import *
from os.path import join
from os.path import expanduser
import time
import os


def get_desktop_path():
    """
    get desktop path
    :return:
    """
    return join(expanduser("~"), 'Desktop')


def get_time():
    """
    get current time,eg:2015/08/31_16:00:08

    :return:string of time,%Y%m%d_%H_%M_%S
    """
    time_format = "%Y%m%d_%H_%M_%S"
    return time.strftime(time_format, time.localtime())


class ButtonFunc(object):
    """
    button clickEvent.
    """
    def __init__(self, output):
        self.button_func_map = {
            INSTALL_ID: self.install,
            SCREENSHOT_ID: self.screen_shot,
            DEVICE_INFO_ID: self.get_device_info,
            UNINSTALL_ID: self.uninstall,
            APP_LIST_ID: self.get_app_list,
            SLEEP_ID: self.sleep,
            SHUT_ID: self.shut,
            REBOOT_ID: self.reboot,
        }  # button id 对应的点击事件
        self.output = output
        self.ipa_path = None
        self.uninstall_bundle = uninstall_list[0]
        self.base_command = "./"

    def set_ipa_path(self, ipa_path):
        """
        set ipa path.
        :param ipa_path:
        :return:
        """
        self.ipa_path = ipa_path

    def set_uninstall_bundleid(self, bundleid):
        """
        set uninstall bundleid.
        :param bundleid:
        :return:
        """
        self.uninstall_bundle = bundleid

    def get_button_func(self, id):
        """
        get button func in term of button id.
        :param id:
        :return:
        """
        return self.button_func_map[id]

    def install(self):
        """
        install ipa to device.
        :return:
        """
        if self.ipa_path:  # 判断ipa_path 是否为空
            self.output.AppendText(self.ipa_path + "\n")
            if os.path.exists(self.ipa_path):  # 判断输入的ipa文件是否存在
                command = self.base_command + "ideviceinstaller -i " + self.ipa_path
                run_command(command,self.output)
            else:
                self.output.AppendText(u"\n文件不存在,请重新输入或者选择\n")
        else:
            self.output.AppendText(u"Error:ipa 文件不能为空,请选择或者输入ipa_path \n")

    def uninstall(self):
        """
        uninstall.
        :return:
        """
        self.output.AppendText("choose: " + self.uninstall_bundle + "\n")
        command = self.base_command + "ideviceinstaller -u " + self.uninstall_bundle
        run_command(command,self.output)

    def screen_shot(self):
        """
        screenshot device to the pc desktop.
        :return:
        """
        image_path = join(get_desktop_path(),get_time()) + ".tiff"
        command = self.base_command + "idevicescreenshot " + image_path
        run_command(command,self.output)

    def get_device_info(self):
        """
        get the plugin in device information.
        :return:
        """
        command = self.base_command + "ideviceinfo"
        get_run_result(command,self.output)

    def get_app_list(self):
        """
        get the customer's app installed in device
        :return:
        """
        command = self.base_command + "ideviceinstaller -l"
        run_command(command,self.output)

    def sleep(self):
        """
        set device in sleep mode.
        :return:
        """
        command =self.base_command + "idevicediagnostics sleep"
        run_command(command,self.output)

    def shut(self):
        """
        shut down the device.
        :return:
        """
        command = self.base_command + "idevicediagnostics shutdown"
        run_command(command,self.output)

    def reboot(self):
        """
        reboot the device.
        :return:
        """
        command = self.base_command +  "idevicediagnostics restart"
        run_command(command,self.output)
