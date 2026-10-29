' Open Guardian Kids - Silent Background Runner
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
agentExe = currentDir & "\OGK_Agent\OGK_Agent.exe"

If fso.FileExists(agentExe) Then
    WshShell.Run Chr(34) & agentExe & Chr(34), 0, False
Else
    MsgBox "Khong tim thay tap tin OGK_Agent.exe tai " & agentExe, 16, "Open Guardian Kids"
End If
