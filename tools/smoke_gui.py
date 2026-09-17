"""Smoke-test our own hidden GUI and capture its client area, no desktop capture."""
import ctypes as c
from ctypes import wintypes as w
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from PIL import Image

import argparse
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import project
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--game-dir',type=Path,required=True)
args=parser.parse_args()
ROOT=project.ROOT
GAME=args.game_dir.resolve()
HERE=ROOT/'.local/gui'
HERE.mkdir(parents=True,exist_ok=True)
u=c.WinDLL('user32',use_last_error=True);g=c.WinDLL('gdi32',use_last_error=True)
u.SendMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM];u.SendMessageW.restype=w.LPARAM
u.GetDlgItem.argtypes=[w.HWND,c.c_int];u.GetDlgItem.restype=w.HWND
u.SetWindowTextW.argtypes=[w.HWND,w.LPCWSTR]
u.GetWindowTextW.argtypes=[w.HWND,w.LPWSTR,c.c_int]
u.GetDC.argtypes=[w.HWND];u.GetDC.restype=w.HDC
u.ReleaseDC.argtypes=[w.HWND,w.HDC]
u.GetClientRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
u.PrintWindow.argtypes=[w.HWND,w.HDC,w.UINT]
u.ShowWindow.argtypes=[w.HWND,c.c_int]
u.UpdateWindow.argtypes=[w.HWND]
g.CreateCompatibleDC.argtypes=[w.HDC];g.CreateCompatibleDC.restype=w.HDC
g.CreateCompatibleBitmap.argtypes=[w.HDC,c.c_int,c.c_int];g.CreateCompatibleBitmap.restype=w.HBITMAP
g.SelectObject.argtypes=[w.HDC,w.HGDIOBJ];g.SelectObject.restype=w.HGDIOBJ
g.DeleteObject.argtypes=[w.HGDIOBJ];g.DeleteDC.argtypes=[w.HDC]
g.GetDIBits.argtypes=[w.HDC,w.HBITMAP,w.UINT,w.UINT,c.c_void_p,c.c_void_p,w.UINT]
CALLBACK=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
u.EnumWindows.argtypes=[CALLBACK,w.LPARAM]
u.EnumChildWindows.argtypes=[w.HWND,CALLBACK,w.LPARAM]
u.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
u.IsWindowEnabled.argtypes=[w.HWND]

def text(hwnd):
    buf=c.create_unicode_buffer(4096);u.GetWindowTextW(hwnd,buf,len(buf));return buf.value

def capture(hwnd):
    rect=w.RECT();u.GetClientRect(hwnd,c.byref(rect));width,height=rect.right,rect.bottom
    dc=u.GetDC(hwnd);mem=g.CreateCompatibleDC(dc);bitmap=g.CreateCompatibleBitmap(dc,width,height)
    old=g.SelectObject(mem,bitmap)
    # Show only our own test window, without activating it, for native rendering.
    u.ShowWindow(hwnd,4);u.UpdateWindow(hwnd)
    assert u.PrintWindow(hwnd,mem,1)
    u.ShowWindow(hwnd,0)
    class Info(c.Structure):
        _fields_=[('size',w.DWORD),('width',w.LONG),('height',w.LONG),('planes',w.WORD),('bits',w.WORD),
                  ('compression',w.DWORD),('image',w.DWORD),('xp',w.LONG),('yp',w.LONG),('used',w.DWORD),('important',w.DWORD)]
    info=Info(40,width,-height,1,32,0,0,0,0,0,0);data=c.create_string_buffer(width*height*4)
    g.SelectObject(mem,old)
    assert g.GetDIBits(mem,bitmap,0,height,data,c.byref(info),0)==height
    Image.frombytes('RGB',(width,height),data.raw,'raw','BGRX').save(HERE/'gui-preview.png')
    g.DeleteObject(bitmap);g.DeleteDC(mem);u.ReleaseDC(hwnd,dc)

temp=tempfile.TemporaryDirectory(prefix='gui-test-',dir=HERE);folder=Path(temp.name)
process=None
try:
    expected=project.targets(GAME)[3]
    manifest={'files':[{'file':name} for name in expected]}
    for name in ['START.EXE']+[r['file'] for r in manifest['files']]:shutil.copy2(GAME/name,folder/name)
    startup=subprocess.STARTUPINFO();startup.dwFlags=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    process=subprocess.Popen([str(ROOT/'build/Ishar2-Cestina.exe')],startupinfo=startup)
    windows=[]
    @CALLBACK
    def find(hwnd,_):
        pid=w.DWORD();u.GetWindowThreadProcessId(hwnd,c.byref(pid))
        if pid.value==process.pid and text(hwnd)=='Ishar 2 – čeština '+project.profile()['version']:windows.append(hwnd)
        return True
    deadline=time.monotonic()+10
    while not windows and time.monotonic()<deadline:u.EnumWindows(find,0);time.sleep(.05)
    assert windows,'GUI window did not start';hwnd=windows[0]
    while not u.GetDlgItem(hwnd,103) and time.monotonic()<deadline:time.sleep(.05)
    assert u.GetDlgItem(hwnd,103),'GUI controls did not initialize'
    capture(hwnd)
    folder_text=c.create_unicode_buffer(str(folder))
    u.SendMessageW(u.GetDlgItem(hwnd,100),0xc,0,c.addressof(folder_text))
    for button,source in [(102,None),(103,GAME)]:
        u.SendMessageW(hwnd,0x111,button,0)
        deadline=time.monotonic()+10
        while not u.IsWindowEnabled(u.GetDlgItem(hwnd,button)) and time.monotonic()<deadline:time.sleep(.05)
        assert u.IsWindowEnabled(u.GetDlgItem(hwnd,button)),'GUI operation did not finish'
        @CALLBACK
        def show_status(child,_):
            print('GUI text:',text(child));return True
        u.EnumChildWindows(hwnd,show_status,0)
        for row in manifest['files']:assert (folder/row['file']).read_bytes()==(expected[row['file']] if source is None else (source/row['file']).read_bytes()),row['file']
    print('GUI: native window, Apply button and Restore button passed; screenshot saved.')
finally:
    if process:
        if windows:u.SendMessageW(windows[0],0x10,0,0)
        try:process.wait(timeout=5)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    assert folder.resolve().is_relative_to(HERE.resolve())
    temp.cleanup()
