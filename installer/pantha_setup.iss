#define MyAppName "Pantha Terminal"
#define MyAppExeName "PanthaTerminal.exe"
#define MyAppPublisher "V1LE-FARM"
#define MyAppURL "https://github.com/V1LE-FARM/pantha-terminal"

; Version from GitHub Actions environment (fallback if missing)
#define MyAppVersion GetEnv("PANTHA_VERSION")
#if MyAppVersion == ""
  #define MyAppVersion "v0.0.0"
#endif

[Setup]
AppId={{D9C0E6A2-8E11-4C9B-9E4A-7D2A6A7F9C10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Output EXE goes into repo folder: installer_output
OutputDir=..\installer_output
OutputBaseFilename=PanthaSetup-{#MyAppVersion}

Compression=lzma
SolidCompression=yes

; IMPORTANT: These MUST exist
SetupIconFile=..\assets\icon.ico
WizardImageFile=..\assets\banner.bmp
WizardSmallImageFile=..\assets\banner.bmp

PrivilegesRequired=admin
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; This installs the FULL PyInstaller ONEDIR folder contents
Source: "..\dist\PanthaTerminal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
