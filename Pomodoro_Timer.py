
import wx
import time


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, size=(350, 150))
        panel = wx.Panel(self, wx.ID_ANY)

        self.s_text_MM = wx.StaticText(panel, wx.ID_ANY, '{:>2}'.format(0))
        s_text_colon = wx.StaticText(panel, wx.ID_ANY, ':')
        self.s_text_SS = wx.StaticText(panel, wx.ID_ANY, '{:02}'.format(0))
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.s_text_MM.SetFont(font)
        s_text_colon.SetFont(font)
        self.s_text_SS.SetFont(font)

        button_Work_Start = wx.Button(panel, wx.ID_ANY, '作業 ▶')
        button_Break_Start = wx.Button(panel, wx.ID_ANY, '休憩 ▶')
        button_Pause = wx.Button(panel, wx.ID_ANY, '一時停止')
        button_Stop = wx.Button(panel, wx.ID_ANY, '停止')

        time_layout = wx.BoxSizer(wx.HORIZONTAL)
        time_layout.AddStretchSpacer(prop=1)
        time_layout.Add(self.s_text_MM, proportion=2, flag=wx.ALIGN_CENTER)
        time_layout.Add(s_text_colon, proportion=1, flag=wx.ALIGN_CENTER)
        time_layout.Add(self.s_text_SS, proportion=2, flag=wx.ALIGN_CENTER)
        time_layout.AddStretchSpacer(prop=1)

        operation_layout = wx.GridSizer(rows=2, cols=2, gap=(0,0))
        operation_layout.Add(button_Work_Start, flag=wx.EXPAND)
        operation_layout.Add(button_Pause, flag=wx.EXPAND)
        operation_layout.Add(button_Break_Start, flag=wx.EXPAND)
        operation_layout.Add(button_Stop, flag=wx.EXPAND)

        top_layout = wx.BoxSizer(wx.HORIZONTAL)
        top_layout.Add(time_layout, proportion=2, flag=wx.EXPAND)
        top_layout.Add(operation_layout, proportion=1,flag=wx.EXPAND)

        panel.SetSizer(top_layout)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.main)
        self.timer.Start(1000)
        self.count = 0
        self.base_time = time.time()

        self.Show()

    def main(self, event):
        self.count = self.count + 1
        elapsed_time = int(round(time.time() - self.base_time,0))
        print(self.count, elapsed_time)
        elapsed_time_mm, elapsed_time_ss = divmod(elapsed_time, 60)
        self.s_text_MM.SetLabel('{:>2}'.format(elapsed_time_mm))
        self.s_text_SS.SetLabel('{:02}'.format(elapsed_time_ss))


app = wx.App(False)
frame = MainWindow(None, "Pomodoro Timer")
app.MainLoop()
