'''
Config GUI
Version 0.1.0
Authors: Colbert Maloy
Release: 04/15/2019

Purpose of this script is to allow the user to set up and edit their quicknotes through an easy, user-friendly interface
'''

import wx
import base64

try:
    import configQN0
    import configQN1
    import configQN2
    import configQN3
    import configQN4
except ModuleNotFoundError:
    with open("configQN0.py", "w+") as filecreation:
        filecreation.write("class QN0(): \n\ttitle = 'Placeholder 1' \n\tnote = ['Placeholder Text']")
    with open("configQN1.py", "w+") as filecreation:
        filecreation.write("class QN1(): \n\ttitle = 'Placeholder 2' \n\tnote = ['Placeholder Text']")
    with open("configQN2.py", "w+") as filecreation:
        filecreation.write("class QN2(): \n\ttitle = 'Placeholder 3' \n\tnote = ['Placeholder Text']")
    with open("configQN3.py", "w+") as filecreation:
        filecreation.write("class QN3(): \n\ttitle = 'Placeholder 4' \n\tnote = ['Placeholder Text']")
    with open("configQN4.py", "w+") as filecreation:
        filecreation.write("class QN4(): \n\ttitle = 'Placeholder 5' \n\tnote = ['Placeholder Text']")
finally:
    import configQN0
    import configQN1
    import configQN2
    import configQN3
    import configQN4

APP_EXIT = 1
SHOW_HELP = 2
SHOW_ABOUT = 3

class Config(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(size = wx.Size(475,400), *args, **kwargs)

        self.InitUI()


    def InitUI(self):

        self.InitMainPanel()
        self.InitMenus()

        # self.SetSize((250, 200))
        self.SetTitle('Hasty Config Utility')
        self.Center()
        self.Show(True)


    def InitMainPanel(self):
        panel = wx.Panel(self)

        # add main widgets
        widgets = self.loadWidgets(panel)
        fgs = wx.FlexGridSizer(rows=len(widgets), cols=2, vgap=10, hgap=15)
        fgs.AddMany([(widget) for widget in widgets])

        # add save button box
        self.clear_button = wx.Button(panel, label='Clear', pos=(140, 300), size=(70, 30))
        self.save_button = wx.Button(panel, label='Save', pos=(255, 300), size=(70, 30))
        self.done_button = wx.Button(panel, label='Done', pos=(370, 300), size=(70, 30))
        self.load_button = wx.Button(panel, label='Load', pos=(370, 50), size=(70, 30))

        self.clear_button.Bind( wx.EVT_BUTTON, self.clear_button_onclick)
        self.save_button.Bind( wx.EVT_BUTTON, self.save_button_onclick)
        self.done_button.Bind( wx.EVT_BUTTON, self.done_button_onclick)
        self.load_button.Bind( wx.EVT_BUTTON, self.load_button_onclick)


    def loadWidgets(self, panel):
        widgets = []

        # Quicknote number dropdown panel creation
        qnNumber_label = wx.StaticText(panel, label="Quicknote Choice:", pos=(20, 30))
        self.number_Control = wx.Choice(panel, pos=(140, 30), size=(120, -1), choices=[configQN0.QN0.title, configQN1.QN1.title, configQN2.QN2.title, configQN3.QN3.title, configQN4.QN4.title])

        # Quicknote title text panel creation
        qnTitle_label = wx.StaticText(panel, label='Quicknote Title:', pos=(20, 60))
        self.title_Control = wx.TextCtrl(panel, pos=(140, 60))

        # Quicknote body text panel creation
        qnBody_label = wx.StaticText(panel, label='Quicknote Text:', pos=(20, 90))
        self.body_Control = wx.TextCtrl(panel, style=wx.TE_MULTILINE, pos=(140, 90), size=(300, 200))

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
        help_text = 'This information is used for your quicknotes while using Hasty, please enter your quicknotes in by typing a number in 1-5, the title of the quicknote, and the actual quicknote, then click the "Save" button.'
        dlg = wx.MessageDialog(self, help_text, 'Help', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()


    def ShowAbout(self, e):
        about_text = 'This application is for the setup of your quicknotes. There are 5 quicknote buttons.'
        dlg = wx.MessageDialog(self, about_text, 'About App', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, e):
        self.Close()

    def clear_button_onclick(self, e):

        self.number_Control.SetSelection(-1)
        self.title_Control.SetValue("")
        self.body_Control.SetValue("")

        confirmation_text = 'Quicknote input cleared successfully.'
        dlg = wx.MessageDialog(self, confirmation_text, 'Clear', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()

    def load_button_onclick(self, e):
        if self.number_Control.GetSelection() == 1:
            self.title_Control.SetValue(configQN0.QN0.title)
            self.body_Control.SetValue("\n".join(configQN0.QN0.note))
        elif self.number_Control.GetSelection() == 2:
            self.title_Control.SetValue(configQN1.QN1.title)
            self.body_Control.SetValue("\n".join(configQN1.QN1.note))
        elif self.number_Control.GetSelection() == 3:
            self.title_Control.SetValue(configQN2.QN2.title)
            self.body_Control.SetValue("\n".join(configQN2.QN2.note))
        elif self.number_Control.GetSelection() == 4:
            self.title_Control.SetValue(configQN3.QN3.title)
            self.body_Control.SetValue("\n".join(configQN3.QN3.note))
        elif self.number_Control.GetSelection() == 5:
            self.title_Control.SetValue(configQN4.QN4.title)
            self.body_Control.SetValue("\n".join(configQN4.QN4.note))

    def save_button_onclick(self, e):

        quicknoteNumber = "class QN%s():" % self.number_Control.GetSelection()
        quicknoteTitle = "\ttitle = '%s'" % self.title_Control.GetValue()
        quicknoteBody = "\tnote = %s\n" % self.body_Control.GetValue().split("#")

        ret = [quicknoteNumber, quicknoteTitle, quicknoteBody]
        print ("\n".join(ret))
        # print(ret)

        if self.number_Control.GetSelection() == 1:
            with open('configQN0.py', 'w') as file:
                file.write("\n".join(ret))
                file.close()
        elif self.number_Control.GetSelection() == 2:
            with open('configQN1.py', 'w') as file:
                file.write("\n".join(ret))
                file.close()
        elif self.number_Control.GetSelection() == 3:
            with open('configQN2.py', 'w') as file:
                file.write("\n".join(ret))
                file.close()
        elif self.number_Control.GetSelection() == 4:
            with open('configQN3.py', 'w') as file:
                file.write("\n".join(ret))
                file.close()
        elif self.number_Control.GetSelection() == 5:
            with open('configQN4.py', 'w') as file:
                file.write("\n".join(ret))
                file.close()

        confirmation_text = 'Your quicknote was updated successfully!'
        dlg = wx.MessageDialog(self, confirmation_text, 'Success', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()

    def done_button_onclick(self, e):
        self.Close()

def main():

    ex = wx.App()
    Config(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
