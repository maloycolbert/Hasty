## HASTY

 ##
## A GUI Assistant for Liberty University's Helpdesk Remote Support ##

Creator: Ian S. Pringle (ipringle2)

## Maintainers: Ian S. Pringle, Joseph Langford, Colbert Maloy



###How to Install

- Create a folder named "hasty" (note that its all lowercase). It can be created anywhere on your C drive (except Program Files and Program Files x86 due to permissions of writing new files to the folder)
- Copy all of the files within the Hasty project into the hasty folder you created
- (make sure to copy the files instead of the whole folder because dropbox creates a shortcut if you copy the folder itself over. NOTE: you can copy over the subfolders)
- (In short, just copy all of the contents of the main hasty folder)
- (the shared project folder should be located in a shared dropbox folder).



- Run the python.exe file in your local hasty folder

- Install Python for all users, and check to include it in the PATH.

- Select Custom Install, select Next, and make sure All Users is selected.



- Once python is installed, open an admin powershell window and copy and paste this command into powershell and press enter:

          python -m pip install selenium requests wxPython pyyaml

- If you receive the error requests 2.21.0 has requirement urllib3<1.25,>=1.21.1, but you'll have urllib3 1.25 which is incompatible during the pip install, run this cmd:
          pip install --upgrade urllib3
- re-run the first cmd

- Finally, run the AutoHotKey_setup.exe
- Choose express installation
- Close the window once its installed
- Edit the "Copy Hasty from Dropbox" file with the location of your dropbox folder and the location of your local hasty folder
- (follow the AHK reference picture to know the location of those in the file)

- Once all previous steps have been completed, close the window and r
estart the computer to source all PATH changes



###How to run

- Double click on the RunHasty.bat file located in the hasty folder to run it



###First Run setup

- Upon running Hasty for the first time, You should receive a window to input your Finesse and Argos credentials

- After filling out your credentials, youll receive another window to set up your quicknotes

These quicknotes are buttons found on your documentation tab that allow for easy documentation with common calls you might receive

IMPORTANT: Remember to set up all 5 quicknotes

(If you dont need all 5 quicknotes, you can just put in filler text and title for the ones you dont need)





###How to update
- As long as you set up the AutoHotKey application and file correctly, just run the Copy Hasty from Dropbox file. After its run, restart Hasty

###How to use


When a call is coming in you can press the pickup button. When the pickup button is pressed, the call documentation timer is started,

the username is grabbed from finesse and put into argos and the hasty tool and search button is automatically pressed.

Youll see important information in the main accounts window. You can press the unlock and unexpire button, you can generate and reset 

a random password,
or you can type your own password into the password box. Pressing Get Info shows info from AD, although it looks a bit messy.

I normally use that for the last line which shows if they are expired or not. The documentation tab is where you will document the call.

You can add your own notes, press the quicknote buttons, there is a dropdown for transfers and a dropdown for templates,
and a checkmark

for LMIR and first call resolution. If you want to add a ticket number, just remove the text at the bottom text panel


and replace it with TKT0000000. When youre done with the call, press submit and the call number will show up in the cmd prompt,


and you can press clear to clear everything from both windows



##Credits:

* **Jorge Torres** (jtorres78) - Created the original Helper. A number of the AD functions were created
 with assistance of Jorge's work

* **Joseph Langford** (jlangford7) - Created the Argos and Finesse scrapers

* **Colbert Maloy** (cmaloy) - created the config GUI to allow a user friendly editing of the quicknotes
