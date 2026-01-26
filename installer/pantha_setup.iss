#define MyAppName "Pantha Terminal"
#define MyAppExeName "PanthaTerminal.exe"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Pantha"
#define MyAppURL "https://github.com/V1LE-FARM/pantha-terminal"

[Setup]
AppId={{A7C9A8B4-0F2A-4C5D-9E2A-1A1F9B8D9C01}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir=..\installer_output
OutputBaseFilename=PanthaSetup-Windows
Compression=lzma
SolidCompression=yes

WizardStyle=modern
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

PrivilegesRequired=admin
DisableProgramGroupPage=yes

ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; Flags: unchecked
Name: "startup"; Description: "Run Pantha Terminal when Windows starts"; Flags: unchecked

[Files]
; IMPORTANT: install the whole PyInstaller folder (exe + _internal + everything)
Source: "..\dist\PanthaTerminal\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Startup option (runs on boot)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; \
    Flags: uninsdeletevalue; Tasks: startup

[Run]
; Launch after install
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
