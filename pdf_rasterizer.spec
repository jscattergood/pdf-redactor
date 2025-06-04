# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_rasterizer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'PIL.ImageTk',
        'fitz',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pdf_rasterizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Create a macOS app bundle (optional, comment out if you just want the executable)
app = BUNDLE(
    exe,
    name='PDFRasterizer.app',
    icon=None,
    bundle_identifier='com.scattergood.pdfrasterizer',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PDF Document',
                'CFBundleTypeExtensions': ['pdf'],
                'CFBundleTypeRole': 'Viewer',
            }
        ],
    },
) 