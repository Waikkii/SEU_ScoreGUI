import wx
import requests
import re

req = requests.Session()
class Frame(wx.Frame):
    """Frame class that displays an image."""
    def __init__(self, image, parent=None, id=-1, pos=wx.DefaultPosition, title='Hello, xxxxxx'):
        """Create a Frame instance and display image."""
        temp = image.ConvertToBitmap()
        size = temp.GetWidth()*2, temp.GetHeight()*7
        wx.Frame.__init__(self, parent, id, title, pos, size)
        bmppos = (0,0)
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp, pos=bmppos)
        self.Username = wx.TextCtrl(self, pos=(250, 50), size=(40, 24))
        button = wx.Button(self, label="确定", pos=(330, 50), size=(50, 24))
        wx.StaticText(self, -1, u"请输入验证码", (250, 30))
        self.text = wx.TextCtrl(self, pos=(0, 120), size=(400, 500), style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON, self.openfile, button)
        #code = self.Username.GetValue()

    def openfile(self, event):
        code = self.Username.GetValue()
        data = {
            'password': 'xxxxxxxxxxxxxxxxx',
            'userName': 'xxxxxxxxxxxxxxxxx',
            'vercode': code
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        req.post('http://xk.urp.seu.edu.cn/studentService/system/login.action', data=data, headers=headers)
        scorehtml = req.get('http://xk.urp.seu.edu.cn/studentService/cs/stuServe/studentExamResultQuery.action')
        title = re.findall(r'<title>(.*?)</title>', scorehtml.text)
        if title[0] != '东南大学成绩查询':
            self.error()
        else:
            pattern1 = re.compile(r'>(.*?)</tr>', re.S | re.M)
            pattern2 = re.compile(r'>(.*?)</td>')
            pattern3 = re.compile(r'>(.*?)&nbsp;</td>')
            rowinfo = pattern1.findall(scorehtml.text)
            score = [([0] * 5) for i in range(60)]
            for num in range(2, len(rowinfo)-4):
                hanglie = pattern2.findall(rowinfo[num])
                shuzi = pattern3.findall(rowinfo[num])
                score[num - 1][0] = hanglie[1]
                score[num - 1][1] = hanglie[2]
                score[num - 1][2] = shuzi[0]
                score[num - 1][3] = shuzi[1]
                score[num - 1][4] = shuzi[2]
                #score[num - 1][2] = shuzi[2]
            fp = open('1.txt', 'w')
            #fp.write(str(len(rowinfo))+"\n")
            for ii in range(1, len(rowinfo)-5):
                if score[ii][0] != 0:
                    fp.write(score[ii][0]+"   "+score[ii][2]+"   "+score[ii][3]+"   "+score[ii][4]+"\n")
                    #####score[ii][0]+"   "+score[ii][1]+"   "+
                    #print(score[ii][0], score[ii][1], score[ii][2])
            fp.close()
            with open('1.txt', "r") as f: 
                self.text.SetValue(f.read())
            #self.text = wx.TextCtrl(self, pos=(0, 120), size=(400, 500), style=wx.TE_MULTILINE)

    def error(self):
        dlg = wx.MessageDialog(None, u"验证错误，请重启软件", u"ERROR", wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

class App(wx.App):
    """Application class."""
    def OnInit(self):
        response = req.get('http://xk.urp.seu.edu.cn/studentService/getCheckCode')
        codeImg = response.content
        fn = open('1.png', 'wb')
        fn.write(codeImg)
        fn.close()
        image = wx.Image('1.png', wx.BITMAP_TYPE_JPEG)
        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():




    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()