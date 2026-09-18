"""End-to-end tests of the actual Windows EXE, on disposable game copies."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import project
GAME=Path(os.environ.get('ISHAR2_GAME_DIR','.')).resolve()
HERE=ROOT/'.local/tests'
RELEASE=ROOT/'build/Ishar2-Cestina.exe'
NAMES=project.profile()['patched_files']
BACKUP='.ishar2-cs-backup-'+project.profile()['version']

@unittest.skipUnless(os.name=='nt' and os.environ.get('ISHAR2_GAME_DIR'),'Requires Windows and ISHAR2_GAME_DIR; no game assets in CI')
class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        HERE.mkdir(parents=True,exist_ok=True)
        cls.expected=project.targets(GAME)[3]
        for name,data in cls.expected.items():
            if hashlib.sha256(data).hexdigest()!=project.profile()['reference_release_sha256'][name]:
                raise AssertionError('Build differs from approved release: '+name)
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='installer-test-',dir=HERE)
        self.game=Path(self.temp.name)/'Hra s češtinou a mezerou'
        self.game.mkdir()
        for name in NAMES+['START.EXE']:shutil.copy2(GAME/name,self.game/name)
        (self.game/'SAVE01.DAT').write_bytes(b'user saved game')
        (self.game/'dosbox.conf').write_bytes(b'user settings')
        self.initial=self.snapshot()
    def tearDown(self):
        assert Path(self.temp.name).resolve().is_relative_to(HERE.resolve())
        self.temp.cleanup()
    def snapshot(self):return {p.name:p.read_bytes() for p in self.game.iterdir() if p.is_file()}
    def run_exe(self,action,ok=True,test=False,env=None,path=None):
        result=subprocess.run([str(ROOT/'build/installer-test.exe' if test else RELEASE),action,str(path or self.game)],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,env=env)
        self.assertEqual(result.returncode,0 if ok else 1,result.stderr.decode('utf-8',errors='replace'))
        return result
    def assert_target(self):
        for name in NAMES:self.assertEqual((self.game/name).read_bytes(),self.expected[name],name)
        for name in ['START.EXE','SAVE01.DAT','dosbox.conf']:self.assertEqual((self.game/name).read_bytes(),self.initial[name])
    def test_install_exact_release_and_restore(self):
        self.run_exe('--check');self.assertFalse((self.game/BACKUP).exists())
        self.run_exe('--apply');self.assert_target()
        for name in NAMES:self.assertEqual((self.game/BACKUP/name).read_bytes(),self.initial[name])
        self.run_exe('--check');self.run_exe('--apply');self.assert_target()
        self.run_exe('--restore');self.assertEqual(self.snapshot(),self.initial)
        self.run_exe('--restore');self.assertEqual(self.snapshot(),self.initial)
        self.run_exe('--apply');self.assert_target()
        self.assertFalse(list(self.game.glob('.ishar2-cs-stage-*')))
    @unittest.skipUnless(os.environ.get('ISHAR2_V10_INSTALLER'),'Optional v1.0 installer required for upgrade test')
    def test_upgrade_via_v10_restore(self):
        old=os.environ['ISHAR2_V10_INSTALLER']
        subprocess.run([old,'--apply',str(self.game)],check=True,timeout=30)
        before=self.snapshot();self.run_exe('--apply',ok=False)
        self.assertEqual(self.snapshot(),before)
        subprocess.run([old,'--restore',str(self.game)],check=True,timeout=30)
        self.assertEqual(self.snapshot(),self.initial)
        self.run_exe('--apply');self.assert_target()
        self.run_exe('--restore');self.assertEqual(self.snapshot(),self.initial)
    def test_wrong_resource_no_mutation(self):
        path=self.game/'PRESENT.IO';path.write_bytes(path.read_bytes()+b'changed')
        before=self.snapshot();self.run_exe('--apply',ok=False)
        self.assertEqual(self.snapshot(),before);self.assertFalse((self.game/BACKUP).exists())
    def test_wrong_exe_no_mutation(self):
        (self.game/'START.EXE').write_bytes(b'unknown executable')
        before=self.snapshot();self.run_exe('--apply',ok=False);self.assertEqual(self.snapshot(),before)
    def test_wrong_folder(self):
        folder=self.game/'empty';folder.mkdir();self.run_exe('--apply',ok=False,path=folder)
        self.assertEqual(list(folder.iterdir()),[])
    def test_corrupt_backup_rejects_restore(self):
        self.run_exe('--apply');(self.game/BACKUP/'MAIN.IO').write_bytes(b'corrupt backup')
        before=self.snapshot();self.run_exe('--restore',ok=False);self.assertEqual(self.snapshot(),before)
    def test_partial_install_resumes_or_restores(self):
        self.run_exe('--apply');(self.game/'MAIN.IO').write_bytes(self.initial['MAIN.IO'])
        self.run_exe('--apply');self.assert_target()
        (self.game/'MAIN.IO').write_bytes(self.initial['MAIN.IO'])
        self.run_exe('--restore');self.assertEqual(self.snapshot(),self.initial)
    def test_partial_backup_completes(self):
        backup=self.game/BACKUP;backup.mkdir();(backup/'MAIN.IO').write_bytes(self.initial['MAIN.IO'])
        self.run_exe('--apply');self.assert_target()
    def test_missing_backup_for_patched_resource_rejected(self):
        (self.game/'MAIN.IO').write_bytes(self.expected['MAIN.IO'])
        before=self.snapshot();self.run_exe('--apply',ok=False)
        self.assertEqual(self.snapshot(),before);self.assertFalse((self.game/BACKUP).exists())
    def test_simulated_interruption_rolls_back(self):
        env=dict(os.environ,ISHAR_TEST_FAIL_AFTER_FIRST='1')
        self.run_exe('--apply',ok=False,test=True,env=env)
        self.assertEqual(self.snapshot(),self.initial)
        self.assertFalse(list(self.game.glob('.ishar2-cs-stage-*')))
        self.run_exe('--apply');self.assert_target()
        before=self.snapshot();self.run_exe('--restore',ok=False,test=True,env=env)
        self.assertEqual(self.snapshot(),before)
    def test_real_write_failure_rolls_back(self):
        path=self.game/'MARCHAND.IO'
        self.assertTrue(ctypes.windll.kernel32.SetFileAttributesW(str(path),1))
        try:
            self.run_exe('--apply',ok=False);self.assertEqual(self.snapshot(),self.initial)
        finally:ctypes.windll.kernel32.SetFileAttributesW(str(path),128)
        self.run_exe('--apply');self.assert_target()
    def test_restore_without_backup(self):
        self.run_exe('--restore',ok=False);self.assertEqual(self.snapshot(),self.initial)
    def test_second_installer_lock_rejected(self):
        (self.game/'.ishar2-cs-lock').write_bytes(b'existing lock')
        before=self.snapshot();self.run_exe('--apply',ok=False);self.assertEqual(self.snapshot(),before)

if __name__=='__main__':unittest.main(verbosity=2)
