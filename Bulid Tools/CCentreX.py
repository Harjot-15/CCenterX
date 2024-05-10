import ctypes
import sys
import os
from PyQt5.QtGui import QIcon
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QMessageBox, QAction, QMenuBar, QScrollArea, QFrame, QGridLayout, QCheckBox, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import logging
from ctypes import wintypes


# Constants
APP_NAME = "CCenterX"
APP_VERSION = "2.0"
# Gets Current User For Windows Tools Comand 
current_user = os.getlogin()



def open_all_icons_folder():
    current_user = os.getlogin()
    path_to_folder = f"C:\\Users\\{current_user}\\AppData\\Local\\Packages\\AD2F1837.myHP_v10z8vjag6ke6\\LocalCache\\Roaming\\HP Inc\\HP Accessory Center\\icons"
    subprocess.Popen(['explorer', path_to_folder])
    
def open_icons_folder():
    current_user = os.getlogin()
    path_to_folder = f"C:\\Users\\{current_user}\\AppData\\Local\\Packages\\AD2F1837.myHP_v10z8vjag6ke6\\LocalCache\\InstalledAppIcons"
    subprocess.Popen(['explorer', path_to_folder])


def run_command(command):
    if command == "OPEN_ALL_ICONS_FOLDER":
        open_all_icons_folder()  # Opens the folder containing all icons
    elif command == "OPEN_ICONS_FOLDER":
        open_icons_folder()  # Opens the folder containing icons for the current user
    elif command == "manage_computer_certificate":
        manage_computer_certificate()  # Opens the management console for computer certificates
    elif command == "manage_user_certificate":
        manage_user_certificate()  # Opens the management console for user certificates
    elif command == "open_computer_management":
        open_computer_management()  # Opens Computer Management
    elif command in ["cmd.exe /c chkdsk /f /r", "cmd.exe /c sfc /scannow", "cmd.exe /c DISM /Online /Cleanup-Image /RestoreHealth"]:
        # Show warning dialog and handle as before
        response = show_warning_dialog(command)
        if response == QMessageBox.Yes:
            # User agreed to proceed
            run_command_as_admin(command)
        else:
            # User chose not to proceed
            show_message("Mission Aborted.")
    else:
        # Handling other commands as before
        try:
            subprocess.Popen(['cmd.exe', '/k', command], shell=True)
        except Exception as e:
            show_message(f"Failed to execute command: {e}")

            
def run_network_command(command):
    try:
        # This prepares the command to be entered in the command prompt, waiting for user to press Enter.
        full_command = f'start cmd /k "echo {command} & echo. & echo Press Enter to execute the command above... & pause"'
        os.system(full_command)
        logging.debug("Network command prepared and waiting for user to execute.")
    except Exception as e:
        logging.error("Failed to prepare network command", exc_info=True)
        show_message(f"Failed to prepare network command: {e}")


def run_command_as_admin(command):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {command}", None, 1)
    
def show_warning_dialog(command):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setWindowTitle("Caution")
    msgBox.setText(f"⚠️ Warning: Executing {command} requires administrative privileges and may affect your system.\n\n🔴 Do not close the tool or the command prompt until the operation is complete, as it could cause harm to your computer and may result in a significant mistake, like damage to the machine.\n\n✅ Proceed with caution.")
    
    # Create custom buttons
    yesButton = msgBox.addButton("⛑️ Yes, I Got It !! ⛑️", QMessageBox.YesRole)
    cancelButton = msgBox.addButton(QMessageBox.Cancel)
    
    msgBox.setDefaultButton(cancelButton)
    if dark_mode_enabled:
        msgBox.setStyleSheet("QMessageBox { background-color: #333; color: white; } QMessageBox QPushButton { background-color: #555; color: white; }")
    else:
        msgBox.setStyleSheet("QMessageBox { background-color: #fff; color: black; } QMessageBox QPushButton { background-color: #eee; color: black; }")
    
    msgBox.exec_()

    # Check which button was clicked
    if msgBox.clickedButton() == yesButton:
        return QMessageBox.Yes
    else:
        return QMessageBox.No

    
def show_message(description):
    msgBox = QMessageBox()
    msgBox.setText(description)
    msgBox.setWindowTitle("Information")
    if dark_mode_enabled:
        msgBox.setStyleSheet("""
            QMessageBox { background-color: #333; color: white; }
            QMessageBox QPushButton { background-color: #222; color: white; }
        """)
    else:
        msgBox.setStyleSheet("""
            QMessageBox { background-color: white; color: black; }
            QMessageBox QPushButton { background-color: #ddd; color: black; }
        """)
    msgBox.exec_()

def set_button_styles():
    button_stylesheet = "QPushButton { background-color: rgb(65, 65, 65); color: white; }" if dark_mode_enabled else ""
    for widget in mainWindow.findChildren(QPushButton):
        widget.setStyleSheet(button_stylesheet)

def set_windows_titlebar_color(hwnd, dark):
    # Define the DWM API constants for setting the dark mode
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # Attribute index for setting dark mode
    value = ctypes.c_int(1 if dark else 0)
    
    # Try setting the attribute and check for errors
    result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
        wintypes.HWND(hwnd),
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value)
    )
    if result != 0:
        print(f"Failed to set title bar color, error: {result}")

def toggle_dark_mode(checked):
    global dark_mode_enabled
    dark_mode_enabled = checked
    app.setPalette(dark_palette if checked else light_palette)
    mainWindow.setStyleSheet("QWidget { background-color: #282828; color: white; }" if checked else "")
    
    # Convert the window ID to HWND correctly
    hwnd = int(mainWindow.winId())
    set_windows_titlebar_color(hwnd, checked)
    
    # Update styles for all buttons if needed
    set_button_styles()
    
def manage_computer_certificate():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "mmc.exe", "/s certmgr.msc", None, 1)

def manage_user_certificate():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "mmc.exe", "/s certlm.msc", None, 1)

def open_computer_management():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "compmgmt.msc", None, None, 1)


# Palettes
dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
dark_palette.setColor(QPalette.WindowText, Qt.white)
dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
dark_palette.setColor(QPalette.ToolTipText, Qt.white)
dark_palette.setColor(QPalette.Text, Qt.white)
dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ButtonText, Qt.white)
dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
dark_palette.setColor(QPalette.HighlightedText, Qt.black)

# Initialize QApplication
app = QApplication(sys.argv)
mainWindow = QMainWindow()
light_palette = QApplication.palette()

# Setup the UI and connect signals
dark_mode_toggle = QCheckBox("Dark Mode")
dark_mode_toggle.setChecked(True)
dark_mode_toggle.stateChanged.connect(toggle_dark_mode)
mainWindow.setCentralWidget(dark_mode_toggle)


# Create the main window
mainWindow = QMainWindow()
mainWindow.setWindowTitle('CCentreX') # Set the initial size of the main window
mainWindow.setWindowIcon(QIcon('H.ico'))  # Set the window icon
mainWindow.resize(1000, 660)

central_widget = QWidget()
mainLayout = QVBoxLayout(central_widget)
mainWindow.setCentralWidget(central_widget)

menu_bar = QMenuBar()
# Create a toggle switch for dark mode
dark_mode_toggle = QCheckBox("🌘Dark Mode🌛")
dark_mode_toggle.setChecked(True)  # Initial state
dark_mode_toggle.toggled.connect(toggle_dark_mode)
menu_bar.setCornerWidget(dark_mode_toggle, Qt.TopRightCorner)  # Place at the top right corner
mainWindow.setMenuBar(menu_bar)

scroll_area = QScrollArea()
scroll_widget = QWidget()
scroll_layout = QVBoxLayout(scroll_widget)
scroll_area.setWidgetResizable(True)
scroll_area.setWidget(scroll_widget)
mainLayout.addWidget(scroll_area)

def add_commands(section_name, commands):
    section_label = QLabel(f"<b>{section_name}</b>")
    section_label.setAlignment(Qt.AlignCenter)
    scroll_layout.addWidget(section_label)
    grid_layout = QGridLayout()

    for i, (name, command, description) in enumerate(commands, start=1):
        btn = QPushButton(name)
        btn.clicked.connect(lambda _, c=command: run_command(c))
        info_btn = QPushButton("ℹ️")
        info_btn.clicked.connect(lambda _, d=description: show_message(d))
        info_btn.setFixedSize(32, 32)

        row, col = divmod(i - 1, 2)
        grid_layout.addWidget(btn, row, col * 2)
        grid_layout.addWidget(info_btn, row, col * 2 + 1)

    scroll_layout.addLayout(grid_layout)
    divider = QFrame()
    divider.setFrameShape(QFrame.HLine)
    divider.setFrameShadow(QFrame.Sunken)
    scroll_layout.addWidget(divider)

commands = {
    "🔋 Power Commands": [
            ("Sleep 😴", "rundll32.exe powrprof.dll,SetSuspendState Sleep", "Puts the computer into sleep mode."),
            ("Hibernate 💤", "rundll32.exe PowrProf.dll,SetSuspendState 0,1,0", "Puts the computer into hibernation."),
            ("Restart 🔄", "shutdown /r /t 0", "Restarts the computer immediately."),
            ("Shutdown 🔌", "shutdown /s /t 0", "Shuts down the computer immediately."),
    ],
    "📁 Explorer Shortcuts": [
            ("🎨🎨 All Icons 🎨🎨", "OPEN_ALL_ICONS_FOLDER", "Opens the All Icons folder."),
            ("📷🎨 User Icons 📷🎨", "OPEN_ICONS_FOLDER", "Opens the Icons folder for the current user."),
            ("🪛⚙️🔌 Task Master 🪛⚙️🔌", "explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}", "Opens the Windows Tools folder."),
            ("🛠️🔨⛏️ Windows Tools 🛠️🔨⛏️", f"C:\\Users\\{current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools.lnk", "Opens the Windows Tools folder."),
            ("Open Control Panel 🔧", "control.exe", "Opens the Control Panel."),
            ("Programs Folder 📂", "explorer shell:programs", "Opens the Programs folder."),
            ("Common Programs Folder 🌐", "explorer shell:common programs", "Opens the Common Programs folder."),
            ("Apps Folder 📱", "explorer shell:appsfolder", "Opens the Applications folder."),
            ("Startup Folder (User) 🚀", "explorer shell:startup", "Opens the Startup folder for the current user."),
            ("Startup Folder (All Users) 🌍", "explorer shell:common startup", "Opens the Startup folder for all users."),
            ("SendTo Menu 📤", "explorer shell:sendto", "Opens the SendTo menu."),
            ("Fonts Directory 🖋️", "explorer shell:fonts", "Opens the Fonts directory."),
            ("Taskbar Pinned Folders (Quick Launch) 📌", f"explorer {subprocess.getoutput('echo %APPDATA%')}\\Microsoft\\Internet Explorer\\Quick Launch", "Opens the Taskbar Pinned folders (Quick Launch)."),
    ],
    "🛠️ Maintenance & Repair": [
            ("Check Disk for Errors (chkdsk /f /r) ⚠️", "cmd.exe /c chkdsk /f /r", "Checks the disk for errors and attempts to fix them. Requires restart and can take a long time. Use with caution."),
            ("System File Checker (sfc /scannow) ⏳", "cmd.exe /c sfc /scannow", "Scans for and repairs corrupted system files. May take some time."),
            ("DISM Tool (DISM /Online /Cleanup-Image /RestoreHealth) 🚑", "cmd.exe /c DISM /Online /Cleanup-Image /RestoreHealth", "Repairs the Windows image. Needs internet and takes time. Use with caution."),
            ("System Restore (rstrui) 🕰️", "cmd.exe /c rstrui", "Restores system files to an earlier point in time. Can help fix problems without affecting personal files."),
    ],
    "🔐 Security and Administration": [
            ("Computer Management 🖥️", "open_computer_management", "Opens the Computer Management console to manage system devices, storage, services, and applications."),
            ("Local Security Policy (secpol.msc) 🔒", "secpol.msc", "Adjusts security settings and configures security policies. Not available in Home editions."),
            ("Windows Services (services.msc) 🚦", "services.msc", "Manages Windows services. Start, stop, and configure services. Use with caution."),
            ("Task Scheduler (taskschd.msc) ⏲️", "taskschd.msc", "Creates and manages common tasks that your computer will carry out automatically at the times you specify."),
            ("Manage Computer Certificate 🖧", "manage_computer_certificate", "Opens the computer certificate management console."),
            ("Manage User Certificate 👤", "manage_user_certificate", "Opens the user certificate management console."),
    ],
    "💻 System Commands": [
            ("System Configuration Tool (msconfig) 🛠", "msconfig", "Opens system configuration to modify boot options, services, and startup programs. Use with caution."),
            ("Event Viewer (eventvwr) 📊", "eventvwr", "Views and analyzes event logs. Helpful for troubleshooting."),
            ("Resource Monitor (resmon) 📈", "resmon", "Monitors system resources like CPU, memory, disk, and network usage."),
            ("Disk Cleanup (cleanmgr) 🧹", "cleanmgr", "Frees up space on your hard disk by cleaning up unnecessary files."),
            ("Advanced User Accounts (netplwiz / control userpasswords2) 👤", "netplwiz", "Manages user accounts and passwords."),
            ("Windows Memory Diagnostic (mdsched) 🧠", "mdsched", "Checks your computer for memory problems."),
            ("Device Manager (devmgmt.msc) 🖥️", "devmgmt.msc", "Manages hardware devices and their drivers."),
            ("DirectX Diagnostic Tool (dxdiag) 🎮", "dxdiag", "Diagnoses and provides information about DirectX and the hardware it runs on."),
            ("Group Policy Editor (gpedit.msc) 🔐", "gpedit.msc", "Edits group policies. Available only in Professional and Enterprise editions. Use with caution."),
            ("Windows Security (windowsdefender://home) 🛡️", "start windowsdefender://home", "Opens Windows Security center."),
    ],
    "🌐 Network and Internet": [
            ("IP Configuration (ipconfig /all) 📶", "ipconfig /all", "Displays all current TCP/IP network configuration values."),
            ("Network Connections (ncpa.cpl) 🔌", "ncpa.cpl", "Opens Network Connections for viewing or modifying network settings."),
            ("Ping (Test connectivity) 🏓", "ping google.com", "Tests connectivity with another network device or internet location."),
            ("Traceroute (tracert) 🛤️", "tracert google.com", "Traces the path packets take to reach a host."),
            ("Network Statistics (netstat -an) 📡", "netstat -an", "Displays active network connections and ports."),
    ],
}

dark_mode_enabled = True  # Initial state
toggle_dark_mode(True)  # Set initial palette
for section_name, cmds in commands.items():
    add_commands(section_name, cmds)

set_button_styles()  # Set button styles after initializing dark mode toggle

mainWindow.show()
sys.exit(app.exec_())
