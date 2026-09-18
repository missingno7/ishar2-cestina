"""Tests use only synthetic bytes and public Czech sources; no game required."""
import copy
from pathlib import Path
import random
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import project
from resource_codec import pack_a1,unpack
from text_codec import encode,slot_bytes

class SourceTests(unittest.TestCase):
    def test_colon_alignment(self):
        slot=dict(leading_spaces=0,trailing_spaces=0,max_bytes=12,colon_column=11)
        self.assertEqual(slot_bytes('Level:',slot)[0],b'L evel     :')
        self.assertEqual(slot_bytes('Úroveň:',slot)[0].index(b':'),11)
        self.assertEqual(slot_bytes('Level:',{k:v for k,v in slot.items() if k!='colon_column'})[0],b'L evel:     ')
        for text in ('Level','Level: x','Level::'):
            with self.assertRaises(ValueError):slot_bytes(text,slot)
        with self.assertRaises(ValueError):slot_bytes('Level:',dict(slot,colon_column=4))
        with self.assertRaises(ValueError):slot_bytes('Level:',dict(slot,colon_column=12))
    def test_translation_complete(self):
        units,slots=project.validate()
        self.assertEqual(len(units),392);self.assertEqual(len(slots),550)
    def test_codec_and_limits(self):
        self.assertEqual(encode('Český kůň')[1],'Český kůň')
        self.assertEqual(encode('ČŽ')[0],b'\x24 \x5e ')
        self.assertEqual(encode('ÁÚŠ')[0],b'A \x7d\x2a')
        self.assertEqual(encode('Úroveň Štít Á')[1],'úroveň štít A')
        self.assertEqual(len(encode('ČŽ')[0]),len(encode('CZ')[0]))
        self.assertEqual(encode('ě')[0],encode('e\u030c')[0])
        for text in ('bad\nline','€','/','#'):
            with self.assertRaises(ValueError):encode(text)
        with self.assertRaises(ValueError):slot_bytes('ABC',dict(leading_spaces=0,trailing_spaces=0,max_bytes=5))
    def test_duplicate_and_changed_numbers_rejected(self):
        real_load=project.load;source=real_load(project.ROOT/'translation/cs.json')
        def fake(path):return source if Path(path)==project.ROOT/'translation/cs.json' else real_load(path)
        source['units'].append(copy.deepcopy(source['units'][0]))
        with patch.object(project,'load',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'Duplicate'):project.validate()
        source['units'].pop()
        row=next(r for r in source['units'] if r['id']=='menu.language_name');row['lines'][0]['cs']='2 - Čeština'
        with patch.object(project,'load',side_effect=fake):
            with self.assertRaises(ValueError):project.validate()
    def test_hand_count_terms_cannot_be_swapped(self):
        real_load=project.load
        source=real_load(project.ROOT/'translation/cs.json')
        row=next(r for r in source['units'] if r['id']=='message.000736')
        row['cs']='Obouruční zbraně:'
        row['lines'][0]['cs']='Obouruční zbraně:'
        def fake(path):return source if Path(path)==project.ROOT/'translation/cs.json' else real_load(path)
        with patch.object(project,'load',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'missing glossary form jednoruční zbraně'):
                project.validate()
    def test_resource_roundtrip(self):
        randomizer=random.Random(63)
        for header in (6,22):
            for data in (b'A',randomizer.randbytes(2048),bytes(range(256))*600):
                raw=bytearray(header);raw[:3]=(len(data)+header).to_bytes(3,'little');raw[3]=0xa1
                raw[4:6]=(1 if header==6 else 0).to_bytes(2,'little');raw+=data
                with self.subTest(header=header,length=len(data)):self.assertEqual(unpack(pack_a1(bytes(raw))),raw)
    def test_truncation_rejected(self):
        with self.assertRaises(ValueError):unpack(b'bad')
        raw=bytearray(6);raw[:3]=(100006).to_bytes(3,'little');raw[3]=0xa1;raw[4]=1
        with self.assertRaises(ValueError):unpack(bytes(raw)+bytes(8))
    def test_pendant_exception_is_scoped_to_club(self):
        real_load=project.load;source=real_load(project.ROOT/'translation/cs.json')
        row=next(r for r in source['units'] if r['id']=='textin.034')
        row['lines'][1]['cs']=row['lines'][1]['cs'].replace('přívěsek','náhrdelník')
        def fake(path):return source if Path(path)==project.ROOT/'translation/cs.json' else real_load(path)
        with patch.object(project,'load',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'missing glossary form přívěsek'):project.validate()
        # A genuine necklace stays a necklace, despite the one reviewed EN error.
        row['lines'][1]['cs']=row['lines'][1]['cs'].replace('náhrdelník','přívěsek')
        row=next(r for r in source['units'] if r['id']=='message.001994')
        row['cs']='přívěsek';row['lines'][0]['cs']='přívěsek'
        with patch.object(project,'load',side_effect=fake):
            with self.assertRaisesRegex(ValueError,'missing glossary form náhrdelník'):project.validate()

if __name__=='__main__':unittest.main()
