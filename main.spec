# -*- mode: python -*-
import shutil

block_cipher = None

added_files = [
         ( r'/home/alk/codes/pyPassGen/recursos_rc.py', 'recursos_rc.py' ),
         ( r'/home/alk/codes/pyPassGen/ui', 'ui' ),
         ]

a = Analysis(['main.py'],
             pathex=['/home/alk/codes/pyPassGen/'],
             datas= added_files,
             hiddenimports=['recursos_rc'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyPassGen.bin',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='/home/alk/codes/pyPassGen/ui/logo.png',
          version='version.txt'
          )

