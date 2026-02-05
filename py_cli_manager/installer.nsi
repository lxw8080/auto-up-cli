; ==============================================================================
; AI CLI 工具管理器 - Windows 安装程序脚本
; 使用 NSIS (Nullsoft Scriptable Install System)
;
; 编译方法:
;   1. 安装 NSIS: https://nsis.sourceforge.io/
;   2. 右键点击此文件，选择 "Compile NSIS Script"
;   3. 或命令行: makensis installer.nsi
; ==============================================================================

!define APP_NAME "AI CLI Manager"
!define APP_EXE_NAME "AI-CLI-Manager.exe"
!define APP_VERSION "1.0.0"
!define COMPANY_NAME "AI CLI Tools"
!define PUBLISHER "AI CLI Manager"

; 安装程序和卸载程序名称
!define INSTALLER_NAME "release\AI-CLI-Manager-Setup-${APP_VERSION}.exe"
!define UNINSTALLER_NAME "uninstall.exe"

; 默认安装目录
!define DEFAULT_DIR "$PROGRAMFILES\${APP_NAME}"

; 定义请求的执行级别（Windows Vista+）
!define EXECUTION_LEVEL "admin"

; ====================================
; 包含现代 UI
; ====================================
!include "MUI2.nsh"

; ====================================
; 安装程序属性
; ====================================
Name "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
InstallDir "${DEFAULT_DIR}"
InstallDirRegKey HKCU "Software\${APP_NAME}" ""
RequestExecutionLevel ${EXECUTION_LEVEL}

; ====================================
; 界面配置
; ====================================
; 显示安装/卸载进度详情
!define MUI_ABORTWARNING
!define MUI_ICON "resources\icon.ico"
!define MUI_UNICON "resources\icon.ico"
!define MUI_HEADERIMAGE
; !define MUI_HEADERIMAGE_BITMAP "resources\header.bmp"  ; 可选: 添加页眉图像

; 欢迎页面
!insertmacro MUI_PAGE_WELCOME
; 许可协议页面 (可选)
; !insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
; 安装目录选择页面
!insertmacro MUI_PAGE_DIRECTORY
; 安装开始菜单项目页面
!insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER
; 安装文件页面
!insertmacro MUI_PAGE_INSTFILES
; 安装完成页面
!insertmacro MUI_PAGE_FINISH

; ====================================
; 卸载程序界面
; ====================================
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; ====================================
; 语言设置
; ====================================
!insertmacro MUI_LANGUAGE "SimpChinese"  ; 简体中文
!insertmacro MUI_LANGUAGE "English"      ; 英文

; ====================================
; 安装程序版本信息
; ====================================
VIProductVersion "${APP_VERSION}.0"
VIAddVersionKey "ProductName" "${APP_NAME}"
VIAddVersionKey "CompanyName" "${COMPANY_NAME}"
VIAddVersionKey "FileDescription" "AI CLI 工具管理器 - Windows 安装程序"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "ProductVersion" "${APP_VERSION}"
VIAddVersionKey "LegalCopyright" "Copyright (C) 2024 ${COMPANY_NAME}"
VIAddVersionKey "OriginalFilename" "${INSTALLER_NAME}"

; ====================================
; 安装部分
; ====================================
Section "主程序" SecMain
    SectionIn RO

    ; 设置输出路径到安装目录
    SetOutPath $INSTDIR

    ; 显示安装详情
    DetailPrint "正在安装 ${APP_NAME} 主程序..."

    ; 复制主程序文件
    File "dist\${APP_EXE_NAME}"

    ; 复制配置文件目录
    CreateDirectory $INSTDIR\config
    File /a "config\tools.json"

    ; 创建配置文件目录 (用于用户自定义配置)
    CreateDirectory $APPDATA\${APP_NAME}\config

    ; 创建开始菜单快捷方式
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
        CreateShortcut "$SMPROGRAMS\$STARTMENU_FOLDER\${APP_NAME}.lnk" \
            "$INSTDIR\${APP_EXE_NAME}" \
            "" \
            "$INSTDIR\${APP_EXE_NAME}" \
            0 \
            SW_SHOWNORMAL \
            "" \
            "AI CLI 工具管理器"
        CreateShortcut "$SMPROGRAMS\$STARTMENU_FOLDER\卸载.lnk" \
            "$INSTDIR\${UNINSTALLER_NAME}"
    !insertmacro MUI_STARTMENU_WRITE_END

    ; 创建桌面快捷方式 (可选，默认勾选)
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" \
        "$INSTDIR\${APP_EXE_NAME}" \
        "" \
        "$INSTDIR\${APP_EXE_NAME}" \
        0

    ; 注册卸载信息
    WriteRegStr HKCU "Software\${APP_NAME}" "" $INSTDIR
    WriteRegStr HKCU "Software\${APP_NAME}" "Version" "${APP_VERSION}"

    ; 创建卸载程序
    WriteUninstaller "$INSTDIR\${UNINSTALLER_NAME}"

    ; 在"添加/删除程序"中注册
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "Publisher" "${PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "UninstallString" "$INSTDIR\${UNINSTALLER_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "QuietUninstallString" "$INSTDIR\${UNINSTALLER_NAME} /S"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "NoRepair" 1

    ; 设置安装大小 (单位: KB)
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "EstimatedSize" 50000

    DetailPrint "安装完成！"
SectionEnd

; ====================================
; 可选部分: 创建快捷方式
; ====================================
Section /o "创建桌面快捷方式" SecShortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" \
        "$INSTDIR\${APP_EXE_NAME}" \
        "" \
        "$INSTDIR\${APP_EXE_NAME}" \
        0
SectionEnd

; ====================================
; 安装程序描述
; ====================================
LangString DESC_SecMain ${LANG_SIMPCHINESE} "安装 AI CLI 工具管理器主程序"
LangString DESC_SecShortcut ${LANG_SIMPCHINESE} "在桌面创建快捷方式"

LangString DESC_SecMain ${LANG_ENGLISH} "Install AI CLI Manager main program"
LangString DESC_SecShortcut ${LANG_ENGLISH} "Create desktop shortcut"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecShortcut} $(DESC_SecShortcut)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; ====================================
; 卸载程序部分
; ====================================
Section "Uninstall"
    ; 显示卸载详情
    DetailPrint "正在卸载 ${APP_NAME}..."

    ; 删除文件
    Delete "$INSTDIR\${APP_EXE_NAME}"
    Delete "$INSTDIR\${UNINSTALLER_NAME}"
    Delete "$INSTDIR\config\tools.json"
    RMDir "$INSTDIR\config"

    ; 删除快捷方式
    !insertmacro MUI_STARTMENU_GETFOLDER Application $STARTMENU_FOLDER
    Delete "$SMPROGRAMS\$STARTMENU_FOLDER\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\$STARTMENU_FOLDER\卸载.lnk"
    RMDir "$SMPROGRAMS\$STARTMENU_FOLDER"
    Delete "$DESKTOP\${APP_NAME}.lnk"

    ; 删除注册表项
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey /ifempty HKCU "Software\${APP_NAME}"

    ; 删除安装目录 (如果为空)
    RMDir "$INSTDIR"

    DetailPrint "卸载完成！"
SectionEnd

; ====================================
; 安装程序初始化函数
; ====================================
Function .onInit
    ; 检查是否已安装
    ReadRegStr $R0 HKCU "Software\${APP_NAME}" ""
    StrCmp $R0 "" done

    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
        "${APP_NAME} 已经安装。$\n$\n是否要覆盖之前的安装？" \
        IDOK uninst
    Abort

uninst:
    ClearErrors
    ExecWait '$R0\${UNINSTALLER_NAME} _?=$R0'
    IfErrors no_remove_uninstaller done
    no_remove_uninstaller:

done:
FunctionEnd
