from cx_Freeze import setup, Executable

executables = [Executable("DirtyShield\dirty_shield.py", base=None)]

packages = ["argparse", "requests", "queue"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "DirtyShield",
    options = options,
    version = "v0.1",
    description = 'PyScript that gather information about given user',
    executables = executables
)