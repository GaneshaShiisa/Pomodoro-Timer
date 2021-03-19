"""Pomodoro Timer

Pomodoro Timerは、いわゆるポモドーロテクニック用のタイマーアプリケーションです。
25分と5分のタイマーが用意されています。

"""

import time
import wx
import pyautogui
import winsound


class MainWindow(wx.Frame):
    """
    MainWindowはメインのウィンドウ設定
    """
    STATUS_STOP = 0
    STATUS_WORK = 10
    STATUS_WORK_PAUSE = 11
    STATUS_WORK_END = 19
    STATUS_BREAK = 20
    STATUS_BREAK_PAUSE = 21
    STATUS_BREAK_END = 29

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY,
                          title=title, size=(350, 150))
        panel = wx.Panel(self, wx.ID_ANY)

        self.s_text_mm = wx.StaticText(panel, wx.ID_ANY, '{:>2}'.format(0))
        s_text_colon = wx.StaticText(panel, wx.ID_ANY, ':')
        self.s_text_ss = wx.StaticText(panel, wx.ID_ANY, '{:02}'.format(0))
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.s_text_mm.SetFont(font)
        s_text_colon.SetFont(font)
        self.s_text_ss.SetFont(font)

        button_work_start = wx.Button(panel, wx.ID_ANY, '作業 ▶')
        button_break_start = wx.Button(panel, wx.ID_ANY, '休憩 ▶')
        button_pause = wx.Button(panel, wx.ID_ANY, '一時停止')
        button_stop = wx.Button(panel, wx.ID_ANY, '停止')

        button_work_start.Bind(wx.EVT_BUTTON, self.evt_button_work_start)
        button_break_start.Bind(wx.EVT_BUTTON, self.evt_button_break_start)
        button_pause.Bind(wx.EVT_BUTTON, self.evt_button_pause)
        button_stop.Bind(wx.EVT_BUTTON, self.evt_button_stop)

        time_layout = wx.BoxSizer(wx.HORIZONTAL)
        time_layout.AddStretchSpacer(prop=1)
        time_layout.Add(self.s_text_mm, proportion=2, flag=wx.ALIGN_CENTER)
        time_layout.Add(s_text_colon, proportion=1, flag=wx.ALIGN_CENTER)
        time_layout.Add(self.s_text_ss, proportion=2, flag=wx.ALIGN_CENTER)
        time_layout.AddStretchSpacer(prop=1)

        operation_layout = wx.GridSizer(rows=2, cols=2, gap=(0, 0))
        operation_layout.Add(button_work_start, flag=wx.EXPAND)
        operation_layout.Add(button_pause, flag=wx.EXPAND)
        operation_layout.Add(button_break_start, flag=wx.EXPAND)
        operation_layout.Add(button_stop, flag=wx.EXPAND)

        top_layout = wx.BoxSizer(wx.HORIZONTAL)
        top_layout.Add(time_layout, proportion=2, flag=wx.EXPAND)
        top_layout.Add(operation_layout, proportion=1, flag=wx.EXPAND)

        panel.SetSizer(top_layout)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.main)
        self.timer.Start(1000)
        self.count = 0
        self.base_time = time.time()
        self.pause_time = 0
        self.pause_time_buf = 0
        self.event = ""

        self.previous_position = pyautogui.position()
        self.active_time = time.time()

        self.status = self.STATUS_STOP
        self.flash_count = 0

        self.Show()

    def main(self, event):
        """
        mainは、メイン処理です。
        """
        # print(self.status, self.pause_time_buf)
        self.event = event
        self.count = self.count + 1

        if self.previous_position != pyautogui.position():
            self.previous_position = pyautogui.position()
            self.active_time = time.time()

        if (time.time() - self.active_time) >= 60:
            pyautogui.press("shift")
            self.active_time = time.time()

        if self.status == self.STATUS_WORK_PAUSE or self.status == self.STATUS_BREAK_PAUSE:
            pause_time_tmp = time.time() - self.pause_time_buf
        else:
            pause_time_tmp = 0

        remaining_time = int(
            round(self.base_time + self.pause_time + pause_time_tmp - time.time(), 0))
        if remaining_time < 0:
            remaining_time = 0
            if self.status == self.STATUS_WORK:
                self.status = self.STATUS_WORK_END
                self.flash_count = 0
            elif self.status == self.STATUS_BREAK:
                self.status = self.STATUS_BREAK_END
                self.flash_count = 0

        time_mm, time_ss = divmod(remaining_time, 60)
        self.s_text_mm.SetLabel('{:>2}'.format(time_mm))
        self.s_text_ss.SetLabel('{:02}'.format(time_ss))

        if self.status == self.STATUS_WORK_END:
            self.pause_time = 0
            if self.flash_count == 0:
                winsound.PlaySound("Clock-Alarm05.wav",
                                   winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            self.flash_count += 1
            if self.flash_count % 2 == 1:
                self.SetBackgroundColour("red")
            else:
                self.SetBackgroundColour(wx.NullColour)
            self.Refresh()
            if self.flash_count >= 15:
                winsound.PlaySound(None, winsound.SND_ASYNC)
            # if self.flash_count >= 40:
            #     self.status = self.STATUS_STOP

        if self.status == self.STATUS_BREAK_END:
            self.pause_time = 0
            if self.flash_count == 0:
                winsound.PlaySound("Clock-Alarm05.wav",
                                   winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            self.flash_count += 1
            if self.flash_count % 2 == 1:
                self.SetBackgroundColour("SPRING GREEN")
            else:
                self.SetBackgroundColour(wx.NullColour)
            self.Refresh()
            if self.flash_count >= 10:
                winsound.PlaySound(None, winsound.SND_ASYNC)
                # self.status = self.STATUS_STOP

    def evt_button_work_start(self, event):
        """「work_start」ボタンが押された時の処理
        """
        self.event = event
        if self.status == self.STATUS_WORK_PAUSE:
            self.pause_time += time.time() - self.pause_time_buf
        else:
            self.base_time = time.time() + 25
            self.pause_time = 0
            self.pause_time_buf = 0
        self.SetBackgroundColour(wx.NullColour)
        self.Refresh()
        self.status = self.STATUS_WORK

    def evt_button_break_start(self, event):
        """「break_start」ボタンが押された時の処理
        """
        self.event = event
        if self.status == self.STATUS_BREAK_PAUSE:
            self.pause_time += time.time() - self.pause_time_buf
        else:
            self.base_time = time.time() + 5
            self.pause_time = 0
            self.pause_time_buf = 0

        self.SetBackgroundColour(wx.NullColour)
        self.Refresh()
        self.status = self.STATUS_BREAK

    def evt_button_pause(self, event):
        """「pause」ボタンが押された時の処理
        """
        self.event = event
        if not (self.status == self.STATUS_WORK_PAUSE or self.status == self.STATUS_BREAK_PAUSE):
            self.pause_time_buf = time.time()

        if self.status == self.STATUS_WORK:
            self.status = self.STATUS_WORK_PAUSE
        elif self.status == self.STATUS_BREAK:
            self.status = self.STATUS_BREAK_PAUSE

    def evt_button_stop(self, event):
        """「stop」ボタンが押された時の処理
        """
        self.event = event
        self.SetBackgroundColour(wx.NullColour)
        self.Refresh()
        self.status = self.STATUS_STOP
        self.base_time = time.time()
        self.pause_time = 0
        self.pause_time_buf = 0


app = wx.App(False)
frame = MainWindow(None, "Pomodoro Timer")
app.MainLoop()
