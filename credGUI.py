'''
Cred GUI
Version 0.0.2
Authors: Joseph Langford and Colbert Maloy
Release: 10/12/2018

Purpose of this script is to request user credentials in the Remote Support HelpDesk Helper tool and save them into a yaml file for future use
'''

import wx
import base64

APP_EXIT = 1
SHOW_HELP = 2
SHOW_ABOUT = 3


class Cred(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Cred, self).__init__(*args, **kwargs)

        self.InitUI()


    def InitUI(self):

        self.InitMenus()
        self.InitMainPanel()

        # self.SetSize((250, 200))
        self.SetTitle('Hasty Setup Utility')
        self.Center()
        self.Show(True)


    def InitMainPanel(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        # add main widgets
        widgets = self.loadWidgets(panel)
        fgs = wx.FlexGridSizer(rows=len(widgets), cols=2, vgap=10, hgap=15)
        fgs.AddMany([(widget) for widget in widgets])
        vbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=20)

        # add button box
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(panel, label='OK', size=(70, 30))
        button_box.Add(self.ok_button, flag=wx.RIGHT)
        vbox.Add(button_box, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)
        self.ok_button.Bind( wx.EVT_BUTTON, self.ok_button_onclick )

        # flag=wx.EXPAND|wx.LEFT|wx.RIGHT


    def loadWidgets(self, panel):
        widgets = []

        username_label = wx.StaticText(panel, label='Username')
        self.username_Control = wx.TextCtrl(panel)
        widgets.append(username_label)
        widgets.append(self.username_Control)

        liberty_password_label = wx.StaticText(panel, label='Liberty Password')
        self.liberty_password_Control = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        widgets.append(liberty_password_label)
        widgets.append(self.liberty_password_Control)

        finesse_password_label = wx.StaticText(panel, label='Finesse Password')
        self.finesse_password_Control = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        widgets.append(finesse_password_label)
        widgets.append(self.finesse_password_Control)

        finesse_extension_label = wx.StaticText(panel, label='Extension')
        self.finesse_extension_Control = wx.TextCtrl(panel)
        widgets.append(finesse_extension_label)
        widgets.append(self.finesse_extension_Control)


        return widgets


    def InitMenus(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        quitMenuItem = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(quitMenuItem)
        menubar.Append(fileMenu, '&File')
        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)

        helpMenu = wx.Menu()
        helpMenuItem = wx.MenuItem(helpMenu, SHOW_HELP, '&Help\tCtrl+H')
        aboutMenuItem = wx.MenuItem(helpMenu, SHOW_ABOUT, 'About\tCtrl+A')
        helpMenu.Append(aboutMenuItem)
        helpMenu.Append(helpMenuItem)
        menubar.Append(helpMenu, 'Help')
        self.Bind(wx.EVT_MENU, self.ShowHelp, id=SHOW_HELP)
        self.Bind(wx.EVT_MENU, self.ShowAbout, id=SHOW_ABOUT)

        self.SetMenuBar(menubar)


    def ShowHelp(self, e):
        help_text = 'This information is used for signing you in while using Hasty, please enter your information correctly and click the "OK" button.'
        dlg = wx.MessageDialog(self, help_text, 'Help', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()


    def ShowAbout(self, e):
        about_text = 'This application is for first time setup, and will be used to update your information for the application to automatically sign you in'
        dlg = wx.MessageDialog(self, about_text, 'About App', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()


    def OnQuit(self, e):
        self.Close()

    def ok_button_onclick(self, e):
        # ret = { 'user': {'usr': self.username_Control.GetValue(), 'pwd': self.liberty_password_Control.GetValue(), 'fnpwd': self.finesse_password_Control.GetValue(), 'extension': self.finesse_extension_Control.GetValue()} }
        # ret = {'usr': self.username_Control.GetValue(), 'pwd': self.liberty_password_Control.GetValue(), 'fnpwd': self.finesse_password_Control.GetValue(), 'extension': self.finesse_extension_Control.GetValue()}
        # ret = [self.username_Control.GetValue(), self.liberty_password_Control.GetValue(), self.finesse_password_Control.GetValue(), self.finesse_extension_Control.GetValue()]

        usr = "usr = '%s'" % self.username_Control.GetValue()
        pwd = "pwd = '%s'" % self.liberty_password_Control.GetValue()
        fnpwd = "fnpwd = '%s'" % self.finesse_password_Control.GetValue()
        extension = "extension = '%s'" % self.finesse_extension_Control.GetValue()

        ret = [usr, pwd, fnpwd, extension]

        if not ret[0] or not ret[1] or not ret[2] or not ret[3]:
            rejected_text = 'You left some information out, please try again!'
            dlg = wx.MessageDialog(self, rejected_text, 'Something went wrong', wx.OK)  # wx.OK|wx.ICON_INFORMATION
            result = dlg.ShowModal()
            dlg.Destroy()

        else:
            file = open('cred.py', 'w')

            file.write("\n".join(ret))
            file.close()
            confirmation_text = 'Your information has been updated, you are now ready to use Hasty!'
            dlg = wx.MessageDialog(self, confirmation_text, 'Success', wx.OK)  # wx.OK|wx.ICON_INFORMATION
            result = dlg.ShowModal()
            dlg.Destroy()

            self.Close()


def main():

    ex = wx.App()
    Cred(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
