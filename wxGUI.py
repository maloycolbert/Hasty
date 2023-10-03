'''
Hasty
Version 1.1.5b
Authors: Ian S. Pringle, Joseph Langford, Colbert Maloy
Release: 2018/10/05
'''

import wx
import wx.xrc
import tools.argos.argosScrape as Argos
import tools.finesse.finesseScrape as Finesse
import tools.sn.sn as SN
import credGUI
import cred
import subprocess
import datetime
import signal
import os
import configGUI
import configQN0
import configQN1
import configQN2
import configQN3
import configQN4
import time
import tools.sn.call_templates as call_templates
import tools.sn.transfer_list as transfer_list
import tools.passgen.passgen as passgen
import tools.hdad.adtools as ad
import tools.sn as service_now

import selenium.common.exceptions

mainWin = 1000

class HD_Tools ( wx.Frame ):

	def __init__( self, parent, argos, finesse):
		wx.Frame.__init__ ( self, parent, id = mainWin, title = u"Hasty", pos = wx.DefaultPosition,
							size = wx.Size( 690,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		#Initalize webdrivers as properties
		self.argos = argos
		self.finesse = finesse

		#Allows specification of minimum and maximum window sizes, and window size increments.
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar = wx.MenuBar( 0 )
		self.m_file = wx.Menu()
		self.m_help = wx.Menu()

		# adding functionality to the buttons in the file tab of the menubar
		self.mi_Cred = wx.MenuItem( self.m_file, wx.ID_ANY, u"Credentials", wx.EmptyString, wx.ITEM_NORMAL )
		self.mi_Config = wx.MenuItem( self.m_file, wx.ID_ANY, u"Config", wx.EmptyString, wx.ITEM_NORMAL )
		self.mi_Exit = wx.MenuItem( self.m_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.mi_Help = wx.MenuItem( self.m_help, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self.mi_About = wx.MenuItem( self.m_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )

		# adding menu items to the file tab in Hasty
		self.m_file.Append( self.mi_Cred )
		self.m_file.Append( self.mi_Config )
		self.m_file.Append( self.mi_Exit )
		self.m_help.Append( self.mi_Help )
		self.m_help.Append( self.mi_About )

		self.m_menubar.Append( self.m_file, u"File" )
		self.m_menubar.Append( self.m_help, u"Help" )

		self.SetMenuBar( self.m_menubar )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelAccount = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition,
										wx.DefaultSize, wx.TAB_TRAVERSAL )

		gbSizerAccounts = wx.GridBagSizer( 0, 0 )
		gbSizerAccounts.SetFlexibleDirection( wx.BOTH )
		gbSizerAccounts.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		sbSizerUsername = wx.StaticBoxSizer( wx.StaticBox( self.m_panelAccount, wx.ID_ANY,
											u"Username" ), wx.HORIZONTAL )

		self.m_textUsername = wx.TextCtrl( sbSizerUsername.GetStaticBox(), wx.ID_ANY,
										wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerUsername.Add( self.m_textUsername, 0, wx.ALL, 5 )

		self.m_buttonSearchUsername = wx.Button( sbSizerUsername.GetStaticBox(), wx.ID_ANY,
												u"Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerUsername.Add( self.m_buttonSearchUsername, 0, wx.ALL, 5 )


		gbSizerAccounts.Add( sbSizerUsername, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ),
							wx.EXPAND|wx.LEFT, 5 )

		sbSizerPassword = wx.StaticBoxSizer( wx.StaticBox( self.m_panelAccount, wx.ID_ANY,
											u"Password" ), wx.VERTICAL )

		bSizerPwdTop = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textPasswordReset = wx.TextCtrl( sbSizerPassword.GetStaticBox(), wx.ID_ANY,
												wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPwdTop.Add( self.m_textPasswordReset, 0, wx.ALL, 5 )

		self.m_buttonresetPwd = wx.Button( sbSizerPassword.GetStaticBox(), wx.ID_ANY,
											u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPwdTop.Add( self.m_buttonresetPwd, 0, wx.ALL, 5 )


		sbSizerPassword.Add( bSizerPwdTop, 1, wx.EXPAND, 5 )

		bSizerPwdBottom = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonPasswordDefault = wx.Button( sbSizerPassword.GetStaticBox(), wx.ID_ANY,
												u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPwdBottom.Add( self.m_buttonPasswordDefault, 0, wx.ALL, 5 )


		sbSizerPassword.Add( bSizerPwdBottom, 1, wx.EXPAND, 5 )


		gbSizerAccounts.Add( sbSizerPassword, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ),
							wx.EXPAND|wx.LEFT, 5 )

		sbSizerAccountManagement = wx.StaticBoxSizer( wx.StaticBox( self.m_panelAccount, wx.ID_ANY,
													u"Account Management" ), wx.VERTICAL )

		gSizer1 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_buttonGetInfo = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
											u"Get Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonGetInfo, 0, wx.ALL, 5 )

		self.m_buttonGetGroup = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
											u"Get Groups", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonGetGroup, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonUnlock = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
										u"Unlock", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonUnlock, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonUnexpire = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
											u"Unexpire", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonUnexpire, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonEnable = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
										u"Enable", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonEnable, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonGetAPR = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
										u"Get APR", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonGetAPR, 0, wx.ALL, 5 )

		self.m_buttonAddGroup = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
											u"Add Group", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonAddGroup, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonLock = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
										u"Lock", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonLock, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonExpire = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
										u"Expire", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonExpire, 0, wx.TOP|wx.BOTTOM, 5 )

		self.m_buttonDisable = wx.Button( sbSizerAccountManagement.GetStaticBox(), wx.ID_ANY,
											u"Disable", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_buttonDisable, 0, wx.TOP|wx.BOTTOM, 5 )


		sbSizerAccountManagement.Add( gSizer1, 1, wx.EXPAND, 5 )


		gbSizerAccounts.Add( sbSizerAccountManagement, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ),
							wx.EXPAND, 5)

		bSizerInfo = wx.BoxSizer( wx.VERTICAL )

		bSizerInfo.SetMinSize( wx.Size( 470,30 ) )
		self.m_textInfo = wx.TextCtrl( self.m_panelAccount, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
										wx.DefaultSize, style= wx.TE_MULTILINE | wx.TE_BESTWRAP )
		self.m_textInfo.SetMinSize( wx.Size( 500,300 ) )

		bSizerInfo.Add( self.m_textInfo, 0, wx.ALL, 5 )


		gbSizerAccounts.Add( bSizerInfo, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )

		bSizerUtilities = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonTimerStart = wx.Button( self.m_panelAccount, wx.ID_ANY,
											u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerUtilities.Add( self.m_buttonTimerStart, 0, wx.ALL, 5 )

		self.m_buttonTimerStop = wx.Button( self.m_panelAccount, wx.ID_ANY,
											u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerUtilities.Add( self.m_buttonTimerStop, 0, wx.ALL, 5 )

		self.m_textTimer = wx.TextCtrl( self.m_panelAccount, wx.ID_ANY, wx.EmptyString,
										wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textTimer.SetMinSize( wx.Size( 80,-1 ) )

		bSizerUtilities.Add( self.m_textTimer, 0, wx.ALL, 5 )

		self.m_buttonPickup = wx.Button( self.m_panelAccount, wx.ID_ANY,
										u"Pickup", wx.DefaultPosition, wx.Size(200,25), 0 )
		bSizerUtilities.Add( self.m_buttonPickup, 0, wx.ALL, 5 )

		self.m_buttonHangup = wx.Button( self.m_panelAccount, wx.ID_ANY,
										u"Hangup", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerUtilities.Add( self.m_buttonHangup, 0, wx.ALL, 5 )


		gbSizerAccounts.Add( bSizerUtilities, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		self.m_panelAccount.SetSizer( gbSizerAccounts )
		self.m_panelAccount.Layout()
		gbSizerAccounts.Fit( self.m_panelAccount )
		self.m_notebook.AddPage( self.m_panelAccount, u"Accounts", True )
		self.m_panelDocumentation = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition,
											wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizerDocumentation = wx.GridBagSizer( 0, 0 )
		gbSizerDocumentation.SetFlexibleDirection( wx.BOTH )
		gbSizerDocumentation.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		sbSizerQuickNotes = wx.StaticBoxSizer( wx.StaticBox( self.m_panelDocumentation, wx.ID_ANY,
															u"Quick Notes" ), wx.HORIZONTAL )


		self.m_buttonQuickNote1 = wx.Button( sbSizerQuickNotes.GetStaticBox(), wx.ID_ANY,
											configQN0.QN0.title, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerQuickNotes.Add( self.m_buttonQuickNote1, 0, wx.ALL, 5 )

		self.m_buttonQuickNote2 = wx.Button( sbSizerQuickNotes.GetStaticBox(), wx.ID_ANY,
												configQN1.QN1.title, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerQuickNotes.Add( self.m_buttonQuickNote2, 0, wx.ALL, 5 )

		self.m_buttonQuickNote3 = wx.Button( sbSizerQuickNotes.GetStaticBox(), wx.ID_ANY,
											configQN2.QN2.title, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerQuickNotes.Add( self.m_buttonQuickNote3, 0, wx.ALL, 5 )

		self.m_buttonQuickNote4 = wx.Button( sbSizerQuickNotes.GetStaticBox(), wx.ID_ANY,
		configQN3.QN3.title, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerQuickNotes.Add( self.m_buttonQuickNote4, 0, wx.ALL, 5 )

		self.m_buttonQuickNote5 = wx.Button( sbSizerQuickNotes.GetStaticBox(), wx.ID_ANY,
										configQN4.QN4.title, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerQuickNotes.Add( self.m_buttonQuickNote5, 0, wx.ALL, 5 )


		gbSizerDocumentation.Add( sbSizerQuickNotes, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		sbSizerDocSettings = wx.StaticBoxSizer( wx.StaticBox( self.m_panelDocumentation, wx.ID_ANY,
												u"Doc Settings" ), wx.HORIZONTAL )

		m_choiceTemplateChoices = [""] + sorted(list(call_templates.templates.keys()), key = str.lower)
		self.m_choiceTemplate = wx.Choice( sbSizerDocSettings.GetStaticBox(), wx.ID_ANY,
											wx.DefaultPosition, wx.Size(300,-1), m_choiceTemplateChoices, 0 )
		self.m_choiceTemplate.SetSelection( 0 )
		sbSizerDocSettings.Add( self.m_choiceTemplate, 0, wx.ALL, 5 )

		self.m_checkBoxLMIR = wx.CheckBox( sbSizerDocSettings.GetStaticBox(), wx.ID_ANY,
											u"LMIR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxLMIR.SetValue(False)
		sbSizerDocSettings.Add( self.m_checkBoxLMIR, 0, wx.ALL, 5 )

		self.m_checkBoxHelpDeskDIY = wx.CheckBox( sbSizerDocSettings.GetStaticBox(), wx.ID_ANY,
													u"HD DIY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxHelpDeskDIY.SetValue(False)
		sbSizerDocSettings.Add( self.m_checkBoxHelpDeskDIY, 0, wx.ALL, 5 )

		self.m_checkBoxFirstCallRes = wx.CheckBox( sbSizerDocSettings.GetStaticBox(), wx.ID_ANY,
													u"FCR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxFirstCallRes.SetValue(False)
		sbSizerDocSettings.Add( self.m_checkBoxFirstCallRes, 0, wx.ALL, 5 )

		m_choiceTransferChoices = [""] + sorted(list(transfer_list.transfer_external.keys()), key = str.lower)
		self.m_choiceTransfer = wx.Choice( sbSizerDocSettings.GetStaticBox(), wx.ID_ANY,
										wx.DefaultPosition, wx.Size(150, -1), m_choiceTransferChoices, 0 )
		self.m_choiceTransfer.SetSelection( 0 )
		sbSizerDocSettings.Add( self.m_choiceTransfer, 0, wx.ALL, 5 )


		gbSizerDocumentation.Add( sbSizerDocSettings, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ),
									wx.EXPAND, 5 )

		sbSizerNotes = wx.StaticBoxSizer( wx.StaticBox( self.m_panelDocumentation, wx.ID_ANY,
										u"Notes" ), wx.HORIZONTAL )

		self.m_textDocumentation = wx.TextCtrl( sbSizerNotes.GetStaticBox(), wx.ID_ANY,
												wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
												style=wx.TE_MULTILINE | wx.TE_BESTWRAP )
		self.m_textDocumentation.SetMinSize( wx.Size( 465,375 ) )

		sbSizerNotes.Add( self.m_textDocumentation, 0, wx.ALL, 5 )


		gbSizerDocumentation.Add( sbSizerNotes, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonSubmit = wx.Button( self.m_panelDocumentation, wx.ID_ANY,
										u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_buttonSubmit, 0, wx.ALL, 5 )

		self.m_buttonClear = wx.Button( self.m_panelDocumentation, wx.ID_ANY,
										u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_buttonClear, 0, wx.ALL, 5 )

		m_studentTypeChoices = ["", "Online", "Residential", "Alumni", "Academy", "Prospective"]
		self.m_studentType = wx.Choice( self.m_panelDocumentation, wx.ID_ANY,
											wx.DefaultPosition, wx.Size(100, -1), m_studentTypeChoices, 0 )
		self.m_studentType.SetSelection( 0 )
		bSizer8.Add( self.m_studentType, 0, wx.ALL, 5 )

		m_queueChoices = ["T1 English", "T2 English", "T3 Supervisor", "Chat", "External", "LUCOM Walk-in"]
		self.m_queueType = wx.Choice( self.m_panelDocumentation, wx.ID_ANY,
											wx.DefaultPosition, wx.Size(100, -1), m_queueChoices, 0 )
		self.m_queueType.SetSelection( 0 )
		bSizer8.Add( self.m_queueType, 0, wx.ALL, 5 )

		self.m_textTicket = wx.TextCtrl( self.m_panelDocumentation, wx.ID_ANY,
										u"Ticket#", wx.DefaultPosition, wx.Size(50, -1), 0)
		bSizer8.Add(self.m_textTicket, wx.ALL, 5)


		gbSizerDocumentation.Add( bSizer8, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		self.m_panelDocumentation.SetSizer( gbSizerDocumentation )
		self.m_panelDocumentation.Layout()
		gbSizerDocumentation.Fit( self.m_panelDocumentation )
		self.m_notebook.AddPage( self.m_panelDocumentation, u"Documentation", False )

		bSizer2.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.mi_CredOnMenuSelection, id = self.mi_Cred.GetId() )
		self.Bind( wx.EVT_MENU, self.mi_ConfigOnMenuSelection, id = self.mi_Config.GetId() )
		self.Bind( wx.EVT_MENU, self.mi_ExitOnMenuSelection, id = self.mi_Exit.GetId() )
		self.Bind( wx.EVT_MENU, self.mi_HelpOnMenuSelection, id = self.mi_Help.GetId() )
		self.Bind( wx.EVT_MENU, self.mi_AboutOnMenuSelection, id = self.mi_About.GetId() )
		self.m_buttonSearchUsername.Bind( wx.EVT_BUTTON, self.m_buttonSearchUsernameOnButtonClick )
		self.m_buttonresetPwd.Bind( wx.EVT_BUTTON, self.m_buttonresetPwdOnButtonClick )
		self.m_buttonPasswordDefault.Bind( wx.EVT_BUTTON, self.m_buttonPasswordDefaultOnButtonClick )
		self.m_buttonGetInfo.Bind( wx.EVT_BUTTON, self.m_buttonGetInfoOnButtonClick )
		self.m_buttonGetAPR.Bind( wx.EVT_BUTTON, self.m_buttonGetAPROnButtonClick )
		self.m_buttonUnexpire.Bind( wx.EVT_BUTTON, self.m_buttonUnexpireOnButtonClick )
		self.m_buttonUnlock.Bind( wx.EVT_BUTTON, self.m_buttonUnlockOnButtonClick )
		self.m_buttonEnable.Bind( wx.EVT_BUTTON, self.m_buttonEnableOnButtonClick )
		self.m_buttonGetGroup.Bind( wx.EVT_BUTTON, self.m_buttonGetGroupOnButtonClick )
		self.m_buttonAddGroup.Bind( wx.EVT_BUTTON, self.m_buttonAddGroupOnButtonClick )
		self.m_buttonExpire.Bind( wx.EVT_BUTTON, self.m_buttonExpireOnButtonClick )
		self.m_buttonLock.Bind( wx.EVT_BUTTON, self.m_buttonLockOnButtonClick )
		self.m_buttonDisable.Bind( wx.EVT_BUTTON, self.m_buttonDisableOnButtonClick )
		self.m_buttonTimerStart.Bind( wx.EVT_BUTTON, self.m_buttonTimerStartOnButtonClick )
		self.m_buttonTimerStop.Bind( wx.EVT_BUTTON, self.m_buttonTimerStopOnButtonClick )
		self.m_buttonPickup.Bind( wx.EVT_BUTTON, self.m_buttonPickupOnButtonClick )
		self.m_buttonHangup.Bind( wx.EVT_BUTTON, self.m_buttonHangupOnButtonClick )
		self.m_buttonQuickNote4.Bind( wx.EVT_BUTTON, self.m_buttonQuickNote4OnButtonClick )
		self.m_buttonQuickNote1.Bind( wx.EVT_BUTTON, self.m_buttonQuickNote1OnButtonClick )
		self.m_buttonQuickNote2.Bind( wx.EVT_BUTTON, self.m_buttonQuickNote2OnButtonClick )
		self.m_buttonQuickNote3.Bind( wx.EVT_BUTTON, self.m_buttonQuickNote3OnButtonClick )
		self.m_buttonQuickNote5.Bind( wx.EVT_BUTTON, self.m_buttonQuickNote5OnButtonClick )
		self.m_choiceTemplate.Bind( wx.EVT_CHOICE, self.m_choiceTemplateOnChoice )
		self.m_checkBoxLMIR.Bind( wx.EVT_CHECKBOX, self.m_checkBoxLMIROnCheckBox )
		self.m_checkBoxFirstCallRes.Bind( wx.EVT_CHECKBOX, self.m_checkBoxFirstCallResOnCheckBox )
		self.m_checkBoxHelpDeskDIY.Bind( wx.EVT_CHECKBOX, self.m_checkBoxDIYOnCheckBox )
		self.m_choiceTransfer.Bind( wx.EVT_CHOICE, self.m_choiceTransferOnChoice )
		self.m_buttonSubmit.Bind( wx.EVT_BUTTON, self.m_buttonSubmitOnButtonClick )
		self.m_buttonClear.Bind( wx.EVT_BUTTON, self.m_buttonClearOnButtonClick )
		self.m_studentType.Bind( wx.EVT_CHOICE, self.m_studentTypeOnChoice )
		self.m_queueType.Bind( wx.EVT_CHOICE, self.m_queueTypeOnChoice )

	def __del__( self ):
		pass

	# Virtual event handlers, overide them in your derived class

	def mi_CredOnMenuSelection( self, event ):
		credGUI.main()

	# Config button definition to open the config gui window and set up quicknotes
	def mi_ConfigOnMenuSelection( self, event ):
		configGUI.main()

	# Virtual event handlers, overide them in your derived class
	def mi_ExitOnMenuSelection( self, event ):
		self.argos.quit()
		self.finesse.quit()
		quit()

	def mi_HelpOnMenuSelection( self, event ):
		dlg = wx.MessageDialog(self, "Help", caption="Help", style=wx.OK)

	def mi_AboutOnMenuSelection( self, event ):
		dlg = wx.MessageDialog(self, "About", caption="About", style=wx.OK)

	def m_buttonSearchUsernameOnButtonClick( self, event ):
		self.username = self.m_textUsername.GetValue()
		try:
			self.callerLookup(self.username)

		except selenium.common.exceptions.WebDriverException:
			self.argos = Argos.Helper(cred.usr, cred.pwd)
			self.argos.open()
			time.sleep(3)
			self.callerLookup(self.username)

	def m_buttonresetPwdOnButtonClick( self, event ):
		password = self.m_textPasswordReset.GetValue()
		subprocess.call(["powershell.exe", "Set-ADAccountPassword -Identity '%s' -NewPassword (ConvertTo-SecureString -AsPlainText '%s' -Force)" % (self.m_textUsername.GetValue(), password)])
		self.m_textInfo.write("New password is '%s'\n\n" % password)


	def m_buttonPasswordDefaultOnButtonClick( self, event ):
		self.m_textPasswordReset.SetValue(passgen.getPassword())

	def m_buttonGetInfoOnButtonClick( self, event ):
		self.m_textInfo.write(ad.getinfo(self.m_textUsername.GetValue()) + "\n")

	def m_buttonGetGroupOnButtonClick( self, event ):
		self.m_textInfo.write(ad.getgroups(self.m_textUsername.GetValue()))

	#Not working
	def m_buttonGetAPROnButtonClick( self, event ):
		p = subprocess.Popen(["powershell.exe", "Get-APR '%s'" % (self.username)], stdout=subprocess.PIPE)
		info = p.communicate()
		#y = str(info).split("\\r\\n")
		#self.m_textInfo.write("\n".join(y[3:-3]))
		self.m_textInfo.write(str(info) + "\n")

	def m_buttonUnlockOnButtonClick( self, event ):
		x = ad.unlock(self.m_textUsername.GetValue()) + "\n"
		self.m_textInfo.write(x)

	def m_buttonLockOnButtonClick( self, event ):
		event.Skip()

	def m_buttonUnexpireOnButtonClick( self, event ):
		for i in range(4):
			x = ad.unexpire(self.m_textUsername.GetValue()) + "\n"
		self.m_textInfo.write(x)

	def m_buttonExpireOnButtonClick( self, event ):
		subprocess.call(["powershell.exe", "Set-Expire '%s' Expire" % (self.username)])
		self.m_textInfo.write("Account expired.\n\n")

	def m_buttonEnableOnButtonClick( self, event ):
		subprocess.call(["powershell.exe", "Set-Enable '%s'" % (self.username)])
		self.m_textInfo.write("Account enabled.\n\n")

	def m_buttonDisableOnButtonClick( self, event ):
		subprocess.call(["powershell.exe", "Set-Enable '%s' Disabled" % (self.username)])
		self.m_textInfo.write("Account disabled.\n\n")

	def m_buttonAddGroupOnButtonClick( self, event ):
		event.Skip()

	def m_buttonTimerStartOnButtonClick( self, event ):
		self.timer = Timer()
		self.opened_at = self.timer.openedat()

	def m_buttonTimerStopOnButtonClick( self, event ):
		event.Skip()

	def m_buttonPickupOnButtonClick( self, event ):
		finesse.answerPhone()
		self.timer = Timer()
		self.opened_at = self.timer.openedat()


		self.callerData = finesse.getCaller()
		print(self.callerData)
		if self.callerData['name'] is not "" and self.callerData['name'] is not '-':
			self.username = self.callerData['name']
			self.callerLookup(self.username)
			self.m_textUsername.write(self.username)
		elif self.callerData['luid'] is not "" and self.callerData['luid'] is not '-  ':
			self.luid = self.callerData['luid']
			self.callerLookup(self.luid)
			self.m_textUsername.write(self.luid)
		else:
			self.m_textUsername.write("No username or LUID found in Finesse")

		print(self.callerData)

	def m_buttonHangupOnButtonClick( self, event ):
		finesse.hangup()

	def m_buttonQuickNote1OnButtonClick( self, event ):
		self.m_textDocumentation.write("" .join(configQN0.QN0.note))
		self.m_textDocumentation.write("\n")

	def m_buttonQuickNote2OnButtonClick( self, event ):
		self.m_textDocumentation.write("" .join(configQN1.QN1.note))
		self.m_textDocumentation.write("\n")

	def m_buttonQuickNote3OnButtonClick( self, event ):
		self.m_textDocumentation.write("" .join(configQN2.QN2.note))
		self.m_textDocumentation.write("\n")

	def m_buttonQuickNote4OnButtonClick( self, event ):
		self.m_textDocumentation.write("" .join(configQN3.QN3.note))
		self.m_textDocumentation.write("\n")

	def m_buttonQuickNote5OnButtonClick( self, event ):
		self.m_textDocumentation.write("" .join(configQN4.QN4.note))
		self.m_textDocumentation.write("\n")

	def m_choiceTemplateOnChoice( self, event ):
		event.Skip()

	def m_checkBoxLMIROnCheckBox( self, event ):
		event.Skip()

	def m_checkBoxFirstCallResOnCheckBox( self, event ):
		event.Skip()

	def m_checkBoxDIYOnCheckBox( self, event ):
		event.Skip()

	def m_choiceTransferOnChoice( self, event ):
		event.Skip()

	def m_studentTypeOnChoice( self, event ):
		event.Skip()

	def m_queueTypeOnChoice( self, event ):
		event.Skip()

	def m_buttonSubmitOnButtonClick( self, event ):
		templateIndex = self.m_choiceTemplate.GetSelection()
		if self.m_choiceTemplate.GetSelection() == 0:
		    dlg = wx.MessageDialog(self, 'Please choose a template', 'Error', wx.OK)  # wx.OK|wx.ICON_INFORMATION
		    result = dlg.ShowModal()
		    dlg.Destroy()
		else:
			typeIndex = self.m_studentType.GetSelection()
			queueIndex = self.m_queueType.GetSelection()
			transferIndex = self.m_choiceTransfer.GetSelection()
			call_doc = {'u_template': self.m_choiceTemplate.GetString(templateIndex),
						'u_username': self.username,
						'u_caller': None, #leave this blank
						'u_id_number': self.luid,
						'u_phone_number': self.phone,
						'u_department': None, #leave this blank
						'u_student_type': self.m_studentType.GetString(typeIndex),
						'cmdb_ci': None, #leave this blank
						'assigned_to': cred.usr,
						'time_worked': self.timer.end(),
						'u_queue': self.m_queueType.GetString(queueIndex),
						'call_type': None, #leave this blank
						'u_operating_system': None,
						'short_description': None, #leave this blank
						'work_notes': self.m_textDocumentation.GetValue(),
						'comments': None, #leave this blank
						'u_used_kb': None,
						'u_webex': None,
						'u_firstcall_resolution': None,
						'u_transfer': None, #leave this blanks
						'u_transfer_internal': None, #leave this blank
						'u_transfer_list': None,
						'u_transfer_queue': None,
						'u_complaint': None,
						'u_complaint_comments': None,
						'parent': None,
						'opened_at': self.opened_at
						}

			if self.m_checkBoxFirstCallRes.IsChecked():
				call_doc['u_firstcall_resolution'] = True
			else:
				call_doc['u_firstcall_resolution'] = False

			if self.m_checkBoxHelpDeskDIY.IsChecked():
				call_doc['u_used_kb'] = True
			else:
				call_doc['u_used_kb'] = False

			if self.m_checkBoxLMIR.IsChecked():
				call_doc['u_webex'] = True
			else:
				call_doc['u_webex'] = False

			if self.m_textTicket.GetValue() != "Ticket#" or "":
				call_doc['parent'] = self.m_textTicket.GetValue()

			if typeIndex != 0:
				call_doc['u_student_type'] = self.m_studentType.GetString(typeIndex)

			if queueIndex != 0:
				call_doc['u_student_type'] = self.m_queueType.GetString(queueIndex)

			if transferIndex != 0:
				call_doc['u_transfer_list'] = self.m_choiceTransfer.GetString(transferIndex)
			try:
				call_doc['u_queue']: self.callerData['qu']
			except:
				pass

			print(call_doc)
			SN.fromGUI(call_doc)

			dlg = wx.MessageDialog(self, 'Call Documentation successfully submitted.\nWould you like to clear the documenation?', 'Success', wx.YES_NO)  # wx.OK|wx.ICON_INFORMATION
			result = dlg.ShowModal()
			dlg.Destroy()

			if result == wx.ID_YES:
				self.m_textUsername.SetValue("")
				self.m_textPasswordReset.SetValue("")
				self.m_textInfo.SetValue("")
				self.m_textDocumentation.SetValue("")
				self.m_textTicket.SetValue("Ticket#")
				self.m_studentType.SetSelection( 0 )
				self.m_queueType.SetSelection( 0 )

				self.m_choiceTemplate.SetSelection( 0 )
				self.m_choiceTransfer.SetSelection( 0 )

				self.m_checkBoxFirstCallRes.SetValue( False )
				self.m_checkBoxLMIR.SetValue( False )
				self.m_checkBoxHelpDeskDIY.SetValue( False )

				#noteBook = self.m_notebook
				#noteBook.SetSelection(self.m_panelAccount, u"Accounts")
			else:
				pass

	def m_buttonClearOnButtonClick( self, event ):

		dlg = wx.MessageDialog(self, 'Are you sure you want to clear the documentation?', 'Clear', wx.YES_NO)  # wx.OK|wx.ICON_INFORMATION
		result = dlg.ShowModal()
		dlg.Destroy()

		if result == wx.ID_YES:
			self.m_textUsername.SetValue("")
			self.m_textPasswordReset.SetValue("")
			self.m_textInfo.SetValue("")
			self.m_textDocumentation.SetValue("")
			self.m_textTicket.SetValue("Ticket#")
			self.m_studentType.SetSelection( 0 )
			self.m_queueType.SetSelection( 0 )

			self.m_choiceTemplate.SetSelection( 0 )
			self.m_choiceTransfer.SetSelection( 0 )

			self.m_checkBoxFirstCallRes.SetValue( False )
			self.m_checkBoxLMIR.SetValue( False )
			self.m_checkBoxHelpDeskDIY.SetValue( False )
		else:
			pass

	def callerLookup(self, id):
		#WIP. Need to add when account is not claimed and two other boxes
		# May only need to show the alt names if account isn't claimed however
		self.m_textInfo.write("----- CALLER LOOKUP -----\n")
		usersName = ''
		intPhone = ''
		intNat = ''
		self.lookup = self.argos.search(id)
		print(self.lookup)
		try:
			if self.lookup[0] != []:
				info = self.lookup[0]
				usersName = info[0]
				self.luid = info[1]
				self.username = info[2]
				ssn = info[3]
				dob = info[4]
				zip = info[5]
				adr = info[6]
				nat = info[7]
				self.phone = info[8]
			elif self.lookup[1] != []:
				info = self.lookup[1]
				usersName = info[0]
				self.luid = self.m_textUsername.GetValue()
				self.username = 'ithelpdesk'
				ssn = info[2]
				dob = info[3]
				zip = info[4]
				adr = info[5]
				nat = info[6]
				self.phone = info[7]
			else:
				self.m_textInfo.write("Lookup failed. Try again. ")
				self.m_textInfo.write("If lookup continues to fail, username or LUID may be wrong.\n\n")
				return
		except NameError:
			self.m_textInfo.write("Lookup failed. Try again. ")
			self.m_textInfo.write("If lookup continues to fail, username or LUID may be wrong.\n\n")
			return

		except TypeError:
			self.m_textInfo.write("Lookup failed. Try again. Debug info in Powershell window. ")
			self.m_textInfo.write("If lookup continues to fail, username or LUID may be wrong.\n\n")
			print("Debug info from call pickup")
			print(self.lookup)
			return

		if self.username != 'ithelpdesk':
			self.m_textInfo.write("Name: "    + usersName + "\n")
			self.m_textInfo.write("Username: " + self.username + "\n")
		elif usersName != '':
			try:
				self.m_textInfo.write("Name: "    + usersName + "\n")
			except UnboundLocalError:
				self.m_textInfo.write("LUID: "    + self.luid + "\n")
				self.m_textInfo.write("Phone: "   + self.phone + "\n\n")
				self.m_textInfo.write("SSN: "     + ssn + "\n")
				self.m_textInfo.write("DOB: "     + dob + "\n")
				self.m_textInfo.write("Zip: "     + zip + "\n\n")

		self.m_textInfo.write("LUID: " + self.luid + "\n")
		self.m_textInfo.write("Phone: " + self.phone + "\n\n")
		self.m_textInfo.write("SSN: " + ssn + "\n")
		self.m_textInfo.write("DOB: " + dob + "\n")
		self.m_textInfo.write("Zip: " + zip + "\n\n")


		if intNat != '':
			self.m_textInfo.write("International Country: " + intNat + "\n\n")
		if intPhone != '':
			self.m_textInfo.write("International Phone: " + intPhone + "\n\n")
		try:
			self.m_textInfo.write("Fraud Alert: " + self.lookup[3][0] + "\n")
			self.m_textInfo.write("Legal Action: " + self.lookup[3][1] + "\n")
			self.m_textInfo.write("ASIST Disabled: " + self.lookup[3][2] + "\n")
		except IndexError:
			self.m_textInfo.write("No Fraud, Legal, or ASIST data in Banner\n")
		self.m_textInfo.write("\n")

		if self.lookup[2] != []:
			self.m_textInfo.write("----- ACCOUNT NOTES -----\n")
			umNotes = self.lookup[2]
			length = len(umNotes)
			i = 0
			while i < length - 1:
				self.m_textInfo.write(umNotes[i] + ": " + umNotes[i+1] + "\n")
				i += 2
			self.m_textInfo.write("\n")

class Timer():

	def __init__(self):
		self.start = time.time()

	def openedat(self):
		today = datetime.datetime.now()
		return today.strftime('%Y-%m-%d %I:%M:%S')
		#Currently not working due to the problem in the forums below:
		#https://community.servicenow.com/community?id=community_question&sys_id=32a443e9dbd8dbc01dcaf3231f9619f5
		#https://community.servicenow.com/community?id=community_question&sys_id=01319563dbdf9780fff8a345ca9619e2

	def current(self):
		totalTime = time.time() - self.start
		hours = "00"
		minutes = "00"
		if totalTime > 3600:
			hours = totalTime / 3600
			totalTime = totalTime - (hours * 3600)
			hours = str(hours)
			if len(hours) < 2:
				hours = "0" + hours
		if totalTime > 60:
			minutes = totalTime /60
			totalTime = totalTime - (minutes * 60)
			minutes = str(minutes)
			if len(minutes) < 2:
				minutes = "0" + minutes
		seconds = str(int(totalTime))
		if len(seconds) < 2:
			seconds = "0" + seconds
		return hours + ":" + minutes + ":" + seconds

	def end(self):
		totalTime = int(time.time() - self.start)
		hours = "00"
		minutes = "00"
		if totalTime > 3600:
			hours = int(totalTime / 3600)
			totalTime = totalTime - (hours * 3600)
			hours = str(hours)
			if len(hours) < 2:
				hours = "0" + hours
		if totalTime > 60:
			minutes = int(totalTime /60)
			totalTime = totalTime - (minutes * 60)
			minutes = str(minutes)
			if len(minutes) < 2:
				minutes = "0" + minutes
		seconds = str(int(totalTime))
		if len(seconds) < 2:
			seconds = "0" + seconds
		formattedTime = "1970-01-01 " + hours + ":" + minutes + ":" + seconds
		return formattedTime


argos = 0
argos = Argos.Helper(cred.usr, cred.pwd)
argos.open()

finesse = 0
finesse = Finesse.Actions(cred.usr, cred.fnpwd, cred.extension)
finesse.open()


app = wx.App()
frm = HD_Tools(None, argos, finesse)
frm.Show()
app.MainLoop()
