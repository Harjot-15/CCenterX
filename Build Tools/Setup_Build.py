import sys 
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "ctypes", "subprocess", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],  # Explicitly include PyQt5 modules
    "include_files": ["H.ico"]  # Include your icon file
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for GUI applications

setup(
    name="CCentreX",
    version="2.0",
    description="CCentreX System Utilty",
    options={"build_exe": build_exe_options},
    executables=[Executable("CCentreX.py", base=base, icon="H.ico")]
)
