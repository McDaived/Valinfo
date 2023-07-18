import sys
from cx_Freeze import setup, Executable
from src.constants import version

build_exe_options = {
    "path": sys.path,
    "include_files":['configurator.bat', 'update_valinfo.bat'],
    "packages": ["requests", "colr", "InquirerPy", "websockets", "pypresence", "nest_asyncio", "rich", "websocket_server"],
    "excludes": ["tkinter", "test", "unittest", "pygments", "xmlrpc"]
}

setup(
    name = "Valinfo",
    version = version,
    description='Valinfo - VALORANT API STATUS',
    executables = [Executable("main.py", icon="./icon/icon.ico", target_name="valinfo.exe")],
    options={"build_exe": build_exe_options}
)
