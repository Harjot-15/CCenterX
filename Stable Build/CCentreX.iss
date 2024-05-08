[Setup]
AppName=CCenterX
AppVersion=1.0
DefaultDirName={pf}\CCenterX
DefaultGroupName=CCenterX
UninstallDisplayIcon={app}\CCX.ico
Compression=lzma2
SolidCompression=yes
; Ensure other directives that might hide the directory selection are not set to hide it

[Files]
Source: "build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CCenterX"; Filename: "{app}\CCentreX.exe"
Name: "{group}\Uninstall CCenterX"; Filename: "{uninstallexe}"; Flags: uninsneveruninstall

[Run]
Filename: "{app}\CCentreX.exe"; Description: "Run CCenterX"; Flags: postinstall nowait skipifsilent

[UninstallRun]
Filename: "{uninstallexe}"; Parameters: "/SILENT"
