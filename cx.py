import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "build_exe": "dist",
    "packages": ["os", "numpy", "scipy", "matplotlib", "docx", "openpyxl"],
    "excludes": ["tkinter", "scipy.spatial.cKDTree"],
    "includes": [
        "matplotlib.backends.backend_qt5agg",
        "matplotlib.dviread",
        "matplotlib.tight_bbox"
    ],
    "include_files": [
        # source
        "src/main/python/frames",
        "src/main/python/logic",
        "src/main/python/reports",
        "src/main/python/science",
        "src/main/python/form.py",
        # other
        "src/main/python/science/samples",
        "src/docx/templates/default.docx"
    ]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Health-weather correlation",
      version="1.1",
      description="",
      options={"build_exe": build_exe_options},
      executables=[Executable(script='src/main/python/main.py', base=base)])
