# coding=utf-8
__author__ = 'gucuijuan'
import subprocess
import wx
import get_device_info


def run_command(run_cmd,output):
    run_cmd = run_cmd.split(" ")
    popen = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if popen.poll() is not None and not next_line:
            break
        if len(next_line) != 0:
            wx.CallAfter(output.AppendText, unicode(next_line))
    popen.wait()
    wx.CallAfter(output.AppendText, unicode("\nfinished..."))


def get_run_result(run_cmd,output):
    result = " "
    run_cmd = run_cmd.split(" ")
    popen = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if popen.poll() is not None and not next_line:
            break
        if len(next_line) != 0:
            result += str(next_line)
    popen.wait()
    device = get_device_info.get_device(result)
    info = ""
    for key,value in device.iteritems():
        info += unicode(key) + ": " + unicode(value) + "\n"
    wx.CallAfter(output.AppendText, info + "\nfinished...")



