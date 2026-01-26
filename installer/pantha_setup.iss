#define MyAppName "Pantha Terminal"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Pantha"
#define MyAppExeName "PanthaTerminal.exe"

[Setup]
AppId={{A1C4D0B1-7E2A-4C91-9F11-11PANTHA0001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Pantha Terminal
DefaultGroupName=Pantha Terminal

OutputDir={#SourcePath}\installer_output
OutputBaseFilename=PanthaSetup

Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes

SetupIconFile={#SourcePath}\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "{#SourcePath}\dist\PanthaTerminal.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; Flags: unchecked

[Icons]
Name: "{group}\Pantha Terminal"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\Pantha Terminal"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Pantha Terminal"; Flags: nowait postinstall skipifsilent
