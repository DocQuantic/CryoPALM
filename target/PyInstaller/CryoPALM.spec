# -*- mode: python -*-

block_cipher = None


a = Analysis(['K:\\STAFF\\PHOTON_TEAM\\Magrini_William\\Dev\\Python\\CryoPALM\\src\\main\\python\\main.py'],
             pathex=['K:\\STAFF\\PHOTON_TEAM\\Magrini_William\\Dev\\Python\\CryoPALM\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['k:\\staff\\photon_team\\magrini_william\\dev\\python\\cryopalm\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['K:\\STAFF\\PHOTON_TEAM\\Magrini_William\\Dev\\Python\\CryoPALM\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='CryoPALM',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='K:\\STAFF\\PHOTON_TEAM\\Magrini_William\\Dev\\Python\\CryoPALM\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='CryoPALM')
