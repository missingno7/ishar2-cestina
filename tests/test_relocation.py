"""Synthetic relocation tests; no original game data."""
from pathlib import Path
import sys,hashlib,unittest,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from relocation import relocate,jump

class RelocationTests(unittest.TestCase):
    def fixture(self,suffix):
        raw=bytearray(b'\0'*8+b'\x1e\x04abc'+suffix+b'\x11'*10)
        resume=13+len(suffix)
        slot=dict(offset=10,max_bytes=3,leading_spaces=0,trailing_spaces=0,
                  relocation=dict(start=8,resume=resume,instruction_sha256=hashlib.sha256(raw[8:resume]).hexdigest(),max_bytes=12,retained_cs='xyz'))
        return raw,slot
    def test_supported_destinations(self):
        for suffix in [b'\0\x16\x42',b'\0\x0a\x16\x01',b'\0\x38\x00\x00\x3a\x18\x34']:
            with self.subTest(suffix=suffix):
                raw,slot=self.fixture(suffix);before=bytes(raw);trailer=len(raw)
                relocate(raw,slot,b'longer name')
                self.assertEqual(raw[8:12],jump(8,trailer))
                self.assertEqual(raw[trailer:trailer+2],b'\x1e\x04')
                self.assertEqual(raw[trailer+2:trailer+13],b'longer name')
                self.assertEqual(raw[trailer+13:-4],suffix)
                self.assertEqual(raw[-4:],jump(len(raw)-4,slot['relocation']['resume']))
                self.assertEqual(raw[slot['relocation']['resume']:trailer],before[slot['relocation']['resume']:])
                self.assertEqual(int.from_bytes(raw[:3],'little'),len(raw))
    def test_rejections_do_not_mutate(self):
        for mode in ['hash','shape','nul','overflow','bounds','segment']:
            raw,slot=self.fixture(b'\0\x16\x42');text=b'longer'
            if mode=='hash':slot['relocation']['instruction_sha256']='0'*64
            if mode=='shape':
                raw[14]=0xff;slot['relocation']['instruction_sha256']=hashlib.sha256(raw[8:16]).hexdigest()
            if mode=='nul':text=b'a\0b'
            if mode=='overflow':text=b'x'*13
            if mode=='bounds':slot['relocation']['start']=7
            if mode=='segment':raw.extend(bytes(65536-len(raw)))
            before=bytes(raw)
            with self.subTest(mode=mode),self.assertRaises(ValueError):relocate(raw,slot,text)
            self.assertEqual(bytes(raw),before)
