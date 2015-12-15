# coding=utf-8
__author__ = 'gucuijuan'
import threading
from button_func import *
import wx
from os.path import join
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
tool_des = [u"安装ipa文件到iPhone手机", u"手机设备截图到电脑桌面",
            u"查看设备的信息包括udid，系统版本等",
            u"卸载应用", u"查看手机上安装了哪些应用", u"休眠", u"关机", u"重启"]  # 功能说明
tool_buttons = {
    INSTALL_ID: u"安装ipa文件",
    SCREENSHOT_ID: u"截图到电脑",
    DEVICE_INFO_ID: u"查看设备信息(udid等)",
    UNINSTALL_ID: u"卸载应用",
    APP_LIST_ID: u"手机应用列表",
    SLEEP_ID: u"休眠",
    SHUT_ID: u"关机",
    REBOOT_ID: u"重启",
}  # map 定义button id 对应的button 名称
use_des = u"安装ipa文件： 需要先选择ipa文件或者手动输入ipa文件路径,选择文件已做过滤只能选择*.ipa\n\n 卸载应用： 可选择要卸载com.elong.hotel 或者com.elong.app,默认选择com.elong.hotel\n\n其他直接点击运行 \n\n备注:截图需要手机添加证书"  # 使用说明


def get_about_tool():
    """
    get tool describe.
    :return:String of about_tool
    """
    about_tool = u"你可以使用它完成如下："
    for index in range(tool_des.__len__()):
        about_tool += "\n" + str(index + 1) + " " + tool_des[index]
    return about_tool


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700, 400))
        self.CreateStatusBar()
        about_menu = wx.Menu()
        menu_about = about_menu.Append(-1, u"&关于iOSTool", " Information about this program") # 定义关于的menu
        menu_exit = about_menu.Append(wx.wx.ID_EXIT, u"退出", "Terminate the program") # 定义退出的menu
        menu_use = about_menu.Append(-1, u"&使用说明", u"使用说明") # 定义使用说明
        menu_bar = wx.MenuBar()
        menu_bar.Append(about_menu, u"&关于")  # MenuBar添加menu
        self.SetMenuBar(menu_bar)
        # Set events.
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)  # 绑定关于的事件
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)  # 绑定退出的事件
        self.Bind(wx.EVT_MENU, self.use_describe, menu_use)  # 绑定使用说明的事件

        # 纵向的功能button
        self.sizer_buttons = wx.BoxSizer(wx.VERTICAL)
        self.buttons = []
        index = 0
        for key,value in tool_buttons.iteritems():
            self.buttons.append(wx.Button(self,key,value))
            self.sizer_buttons.Add(wx.StaticText(self),1,wx.EXPAND)
            self.sizer_buttons.Add(self.buttons[index],1, wx.EXPAND)
            index +=1
        self.sizer_buttons.Add(wx.StaticText(self),1,wx.EXPAND)

        # 功能button 绑定事件
        for button in self.buttons:
            self.Bind(wx.EVT_BUTTON,self.on_click,button)

        # 定义panel 展示参数和输出结果
        self.panel = wx.Panel(self)
        self.ipa_des = wx.StaticText(self.panel, label=u"ipa文件:", pos=(20, 30))
        self.ipa_path_text = wx.TextCtrl(self.panel, value=u"选择或者手动输入ipa文件路径", pos=(130, 30), size=(180, -1))
        self.ipa_choose = wx.Button(self.panel, wx.ID_OPEN, u"选择ipa文件", pos=(320, 25))
        self.Bind(wx.EVT_BUTTON, self.on_open, self.ipa_choose)
        self.Bind(wx.EVT_TEXT,self.modify_ipa_path,self.ipa_path_text)

        self.uninstall_des = wx.StaticText(self.panel, label=u"选择要卸载的应用:", pos=(20, 70))
        # the combobox Control
        self.uninstall_bundleid = wx.ComboBox(self.panel, pos=(130, 70), size=(180, -1), choices=uninstall_list, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.choose_uninstall_package, self.uninstall_bundleid)

        # self.uninstall_package = wx.TextCtrl(self.panel, value="eg:com.elong.app", pos=(90, 70),
        #                                      size=(180, -1))
        self.output = wx.TextCtrl(self.panel,value=u"结果输出...",pos=(20, 120),
                                             size=(390, 200),style=(wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_DONTWRAP))

        # 加入sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.block = wx.StaticText(self)
        self.sizer.Add(self.block,1,wx.EXPAND)
        self.sizer.Add(self.sizer_buttons, 6, wx.EXPAND)
        self.sizer.Add(self.panel, 18, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)
        self.func = ButtonFunc(self.output)

    def on_about(self, e):
        dlg = wx.MessageDialog(self, "A small Tool for iOS By gucuijuan", get_about_tool(), wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def use_describe(self, e):
        dlg = wx.MessageDialog(self, "How To Use", use_des, wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def on_exit(self, e):
        self.Close(True)

    def on_open(self, e):
        """ Open a file"""
        self.dir_name = ''
        dlg = wx.FileDialog(self, "Choose a file",get_desktop_path(), "", "*.ipa", wx.OPEN) # 智能选择 *.ipa
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name = dlg.GetFilename()
            self.dir_name = dlg.GetDirectory()
            ipa_path = join(self.dir_name, self.file_name)
            self.ipa_path_text.SetValue(ipa_path)
            self.func.set_ipa_path(ipa_path)
            dlg.Destroy()

    def on_click(self,e):
        self.output.SetValue(unicode(e.GetEventObject().GetLabelText()) + " start...\n\n")
        button_click = self.func.get_button_func(e.GetId())
        t = threading.Thread(target=button_click,args=())
        t.setDaemon(True)
        t.start()
        # button_click()

    def choose_uninstall_package(self,e):
        self.func.set_uninstall_bundleid(str(e.GetString()))

    def modify_ipa_path(self,e):
        ipa_path = e.GetString()
        self.func.set_ipa_path(ipa_path)


app = wx.App(False)
frame = MainWindow(None, "iOSTool")
frame.Show(True)
app.MainLoop()




