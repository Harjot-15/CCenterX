[Setup]
AppName=CCenterX
AppVersion=2.0
DefaultDirName={pf}\CCenterX
DefaultGroupName=CCenterX
UninstallDisplayIcon={app}\H.ico
Compression=lzma2
SolidCompression=yes
; Ensure other directives that might hide the directory selection are not set to hide it
DisableDirPage=no  
; Ensure the directory selection page is enabled

[Files]
Source: "build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CCenterX"; Filename: "{app}\CCentreX.exe"
Name: "{group}\Uninstall CCenterX"; Filename: "{uninstallexe}"; Flags: uninsneveruninstall

[Run]
Filename: "{app}\CCentreX.exe"; Description: "Run CCenterX"; Flags: postinstall nowait skipifsilent

[UninstallRun]
Filename: "{uninstallexe}"; Parameters: "/SILENT"