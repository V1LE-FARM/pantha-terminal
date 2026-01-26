#define MyAppName "Pantha Terminal"
#define MyAppExeName "PanthaTerminal.exe"
#define MyAppPublisher "Pantha"
#define MyAppURL "https://github.com/V1LE-FARM/pantha-terminal"

#define MyAppVersion GetEnv("PANTHA_VERSION")
#if MyAppVersion == ""
  #define MyAppVersion "v0.0.0"
#endif

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

; IMPORTANT: This must be inside the repo for GitHub Actions
OutputDir=installer_output
OutputBaseFilename=PanthaSetup-Windows-{#MyAppVersion}

Compression=lzma
SolidCompression=yes
WizardStyle=modern

SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

WizardResizable=no
DisableProgramGroupPage=yes

PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

UsePreviousAppDir=yes
UsePreviousGroup=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; Flags: unchecked
Name: "startup"; Description: "Run Pantha Terminal when Windows starts"; Flags: unchecked
Name: "debugshortcut"; Description: "Create a Debug shortcut (keeps console open)"; Flags: unchecked

[Files]
; Install the full PyInstaller ONEDIR folder
Source: "dist\PanthaTerminal\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
; Normal shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Debug shortcut (runs via cmd.exe /k so it stays open on crash)
Name: "{group}\{#MyAppName} (Debug)"; \
  Filename: "{cmd}"; \
  Parameters: "/k ""cd /d ""{app}"" && ""{app}\{#MyAppExeName}"""""; \
  WorkingDir: "{app}"; \
  Tasks: debugshortcut

Name: "{commondesktop}\{#MyAppName} (Debug)"; \
  Filename: "{cmd}"; \
  Parameters: "/k ""cd /d ""{app}"" && ""{app}\{#MyAppExeName}"""""; \
  WorkingDir: "{app}"; \
  Tasks: debugshortcut

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; \
  Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
