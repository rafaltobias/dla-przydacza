# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['chromium.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Rafał/Downloads/chrome/chromedriver-win64/chromedriver.exe', '.'), ('C:/Users/Rafał/Downloads/Proton-VPN-Fast-Secure-Chrome-Web-Store.crx', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='chromium',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
