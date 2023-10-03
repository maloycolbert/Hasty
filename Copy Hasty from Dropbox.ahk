#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


;==============
; Version updater (Download content from 4307)
;==============


MsgBox, 49,File Upload,  `nDo you want to Overwrite folder content?
	IfMsgBox OK
{
	; The following example copies all files and folders inside a folder to a different folder:
	ErrorCount := CopyFilesAndFolders("C:\Users\cmaloy\Dropbox (Liberty University)\hasty\*.*", "C:\tools\hasty")
	if ErrorCount <> 0
		MsgBox %ErrorCount% files/folders could not be copied.
	MsgBox Download Completed.  Restart the application please.
	Sleep, 200
}
return


CopyFilesAndFolders(SourcePattern, DestinationFolder, DoOverwrite = 1)
; Copies all files and folders matching SourcePattern into the folder named DestinationFolder and
; returns the number of files/folders that could not be copied.
{
    ; First copy all the files (but not the folders):
    FileCopy, %SourcePattern%, %DestinationFolder%, %DoOverwrite%
	;FileCopy, %SourcePattern%, %DestinationFolder%, 1
    ErrorCount := ErrorLevel
	if ErrorLevel  
            MsgBox Could not copy %A_LoopFileFullPath% into %DestinationFolder%.
    ; Now copy all the folders:
    Loop, %SourcePattern%, 2  ; 2 means "retrieve folders only".
    {
        FileCopyDir, %A_LoopFileFullPath%, %DestinationFolder%\%A_LoopFileName%, %DoOverwrite%
        ErrorCount += ErrorLevel
        if ErrorLevel  
            MsgBox Could not copy %A_LoopFileFullPath% into %DestinationFolder%.
    }
    return ErrorCount
}

ExitApp


