"""Public localization build: Unicode sources + a user-supplied original game."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile

from resource_codec import unpack,pack_a1
from text_codec import slot_bytes
from relocation import relocate

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(data):return hashlib.sha256(data).hexdigest()
def profile():return load(ROOT/'metadata/profile.json')
def match(term,text):return re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',text,re.I) is not None
def unique(rows,label):
    result={r['id']:r for r in rows}
    if len(result)!=len(rows):raise ValueError('Duplicate '+label+' ID')
    return result

def validate():
    layout=load(ROOT/'metadata/layout.json')['units']
    source=load(ROOT/'translation/cs.json')['units']
    translations=unique(source,'translation');units=unique(layout,'layout')
    if set(translations)!=set(units):raise ValueError('Missing or unexpected translation unit')
    encoded={};seen=set()
    for uid,u in units.items():
        row=translations[uid]
        if row['status']!='ready' or not row['cs'].strip():raise ValueError(uid+': incomplete translation')
        lines=unique(row['lines'],'line')
        if set(lines)!={s['id'] for s in u['slots']}:raise ValueError(uid+': missing or extra line')
        allnums=[];expected=[]
        for slot in u['slots']:
            sid=slot['id'];text=lines[sid]['cs']
            if sid in seen:raise ValueError('Duplicate target slot '+sid)
            seen.add(sid)
            if not text.strip():raise ValueError(sid+': empty text')
            nums=re.findall(r'\d+(?:[.,]\d+)*',text);allnums+=nums;expected+=slot['numbers']
            if not u['reflow_allowed'] and Counter(nums)!=Counter(slot['numbers']):raise ValueError(sid+': changed numbers')
            if any(not match(token,text) for token in slot['tokens']):raise ValueError(sid+': missing protected token')
            try:
                budget=dict(slot,max_bytes=slot['relocation']['max_bytes']) if 'relocation' in slot else slot
                encoded[sid]=slot_bytes(text,budget)[0]
            except ValueError as error:raise ValueError(sid+': '+str(error)) from error
        if Counter(allnums)!=Counter(expected):raise ValueError(uid+': changed numeric values')
        if uid=='menu.language_name' and row['lines'][0]['cs']!='3 - Čeština':raise ValueError('Language choice must be 3 - Čeština')
    glossary=load(ROOT/'translation/glossary.json')['entries'];unique(glossary,'term')
    for term in glossary:
        if term['status']!='ready' or not term['forms']:raise ValueError(term['id']+': glossary incomplete')
        for uid in term['units']:
            row=translations[uid]
            for text in (row['cs'],' '.join(r['cs'] for r in row['lines'])):
                if not any(match(form,text) for form in term['forms']):raise ValueError(uid+': missing glossary form '+term['cs'])
    return layout,encoded

def originals(game):
    game=Path(game).resolve();p=profile()
    if digest((game/'START.EXE').read_bytes())!=p['exe_sha256']:raise ValueError('Unsupported START.EXE')
    packed={};decoded={}
    for name,row in p['files'].items():
        data=(game/name).read_bytes()
        if digest(data)!=row['sha256']:raise ValueError('Unsupported original '+name)
        raw=unpack(data)
        if len(raw)!=row['decoded_size']:raise ValueError('Wrong decoded size '+name)
        packed[name]=data;decoded[name]=raw
    return packed,decoded

def targets(game):
    layout,encoded=validate();packed,base=originals(game);p=profile()
    buffers={n:bytearray(base[n]) for n in p['patched_files']}
    for name,row in p['native_tail_normalization'].items():buffers[name][row['offset']]=row['value']
    for unit in layout:
        for slot in unit['slots']:
            data=buffers[slot['file']];offset=slot['offset'];length=slot['max_bytes']
            if data[offset+length]!=0:raise ValueError('Missing source terminator '+slot['id'])
            if 'relocation' not in slot:data[offset:offset+length]=encoded[slot['id']]
    relocations={s['id']:s for u in layout for s in u['slots'] if 'relocation' in s}
    order=p.get('relocation_order',[])
    if len(order)!=len(set(order)) or set(order)!=set(relocations):raise ValueError('Invalid relocation order')
    for sid in order:
        slot=relocations[sid];relocate(buffers[slot['file']],slot,encoded[sid])
    for glyph in load(ROOT/'translation/font-delta.json')['glyphs']:
        data=buffers['MAIN.IO'];start=glyph['offset'];width=glyph['width'];height=glyph['height'];seen=set()
        if width!=16 or height not in (10,11,12) or start+width*height//2>len(data):raise ValueError('Invalid glyph geometry')
        for index,value in glyph['pixels']:
            if index in seen or not 0<=index<width*height or not 0<=value<=15:raise ValueError('Invalid glyph pixel delta')
            seen.add(index);offset=start+index//2
            data[offset]=(data[offset]&15)|(value<<4) if index%2==0 else (data[offset]&240)|value
    fix=p['layout_fix'];raw=buffers[fix['file']]
    if raw[fix['offset']]!=fix['before']:raise ValueError('Unexpected dialogue layout')
    raw[fix['offset']]=fix['after'];compiled={}
    for name,raw in buffers.items():
        header=22 if raw[4:6]==b'\0\0' else 6
        raw[3]=0xa1 if len(raw)-header>65535+65521 else 0
        data=pack_a1(bytes(raw)) if raw[3]==0xa1 else bytes(raw)
        if unpack(data)!=raw:raise ValueError('Resource roundtrip failed '+name)
        compiled[name]=data
    return packed,base,{n:bytes(b) for n,b in buffers.items()},compiled

FONT_MAP=str.maketrans({'#':'ä','$':'á','%':'ö','&':'ü','*':'ß','/':'á','<':'à','=':'â','>':'è',
    '[':'é','\\':'ê',']':'ô','^':'ê','_':'î','`':'û','{':'ç','}':'ù'})
def context(game):
    _,base=originals(game)
    def text(ref):
        b=base[ref['file']][ref['offset']:ref['offset']+ref['length']]
        return re.sub(r'([A-Z]) ',r'\1',b.decode('ascii').translate(FONT_MAP))
    rows=[]
    for u in load(ROOT/'metadata/layout.json')['units']:
        rows.append(dict(id=u['id'],english=[text(r) for r in u['english']],
            references={lang:[text(r) for r in refs] for lang,refs in u['references'].items()},slots=u['slots']))
    save(ROOT/'.local/context.json',dict(private=True,units=rows))
    translations={u['id']:u for u in load(ROOT/'translation/cs.json')['units']}
    review=['# Soukromé porovnání EN / DE / FR / CS', '', 'Obsahuje původní herní texty. Nepublikovat.', '']
    for row in rows:
        review.extend(['## '+row['id'], '', 'EN: '+' / '.join(row['english']), ''])
        for lang in ('de','fr'):
            review.extend([lang.upper()+': '+' / '.join(row['references'].get(lang,[])), ''])
        cs=translations[row['id']]
        review.extend(['CS: '+cs['cs'], '', 'Herní řádky:', ''])
        review.extend('- '+line['cs'] for line in cs['lines'])
        review.append('')
    (ROOT/'.local/review-languages.md').write_text('\n'.join(review),encoding='utf-8')
    prompt='Soukromý pracovní podklad; nepublikovat. Uprav český překlad podle anglických referencí, slovníčku a stylu. '
    prompt+='Zachovej ID, čísla, ovládací prvky a limity slotů. Vrať úplný JSON ve stejném formátu jako translation.\n\n'
    prompt+=(ROOT/'docs/TRANSLATION_STYLE.md').read_text(encoding='utf-8')
    prompt+='\n\n```json\n'+json.dumps(dict(context=rows,translation=load(ROOT/'translation/cs.json'),
        glossary=load(ROOT/'translation/glossary.json')),ensure_ascii=False,indent=2)+'\n```\n'
    (ROOT/'.local/translation-request.md').write_text(prompt,encoding='utf-8')
    print('Imported local references to .local/context.json (do not publish).')

def prepare_payload(game):
    packed,base,raw,compiled=targets(game);p=profile();version=p['version']
    if not re.fullmatch(r'[a-zA-Z0-9.-]{1,24}',version):raise ValueError('Invalid release version')
    output=ROOT/'build';output.mkdir(exist_ok=True)
    payload=bytearray(b'ISHCS005')
    def number(n):payload.extend(struct.pack('<I',n))
    number(len(p['patched_files']));audit=[]
    for name in p['patched_files']:
        name_bytes=name.encode('ascii');number(len(name_bytes));payload.extend(name_bytes)
        for data in (packed[name],compiled[name],base[name]):payload.extend(hashlib.sha256(data).digest())
        number(len(raw[name]));hunks=[];i=0
        while i<len(raw[name]):
            if i<len(base[name]) and base[name][i]==raw[name][i]:i+=1;continue
            begin=i
            while i<len(raw[name]) and (i>=len(base[name]) or base[name][i]!=raw[name][i]):i+=1
            hunks.append((begin,raw[name][begin:i]))
        number(len(hunks))
        for offset,data in hunks:number(offset);number(len(data));payload.extend(data)
        audit.append(dict(file=name,sha256=digest(compiled[name]),changed_bytes=sum(len(b) for _,b in hunks),hunks=len(hunks)))
    header='// Generated; do not commit.\nstatic const unsigned char patchData[] = {\n'
    header+='\n'.join(','.join(map(str,payload[i:i+32]))+',' for i in range(0,len(payload),32))+'\n};\n'
    header+='static const wchar_t* patchVersion=L"'+version+'";\n'
    header+='static const wchar_t* backupFolder=L".ishar2-cs-backup-'+version+'";\n'
    header+='static const wchar_t* windowTitle=L"Ishar 2 – čeština '+version+'";\n'
    header+='static const char* supportedExeHash="'+p['exe_sha256']+'";\n'
    (output/'patch_data.h').write_text(header,encoding='utf-8')
    save(output/'manifest.json',dict(version=version,payload_bytes=len(payload),files=audit,
        sources={str(path.relative_to(ROOT)):digest(path.read_bytes()) for folder in ('translation','metadata') for path in sorted((ROOT/folder).glob('*.json'))}))
    print('Prepared',len(payload),'bytes of patch data; original game files were not copied.')
    return output

def build(game,cxx=None,windres=None):
    output=prepare_payload(game)
    compiler=cxx or os.environ.get('CXX') or shutil.which('g++')
    resource_compiler=windres or os.environ.get('WINDRES') or shutil.which('windres')
    if not compiler or not resource_compiler:raise ValueError('MinGW-w64 g++ and windres are required; use --cxx / --windres or PATH')
    subprocess.run([resource_compiler,'app.rc','-O','coff','-o',str(output/'app.res')],cwd=ROOT/'src',check=True)
    args=[compiler,'-std=c++17','-O2','-s','-static','-static-libgcc','-static-libstdc++','-municode','-mwindows',
        '-finput-charset=UTF-8','-I'+str(output),str(ROOT/'src/installer.cpp'),str(output/'app.res'),
        '-lbcrypt','-lole32','-lshell32','-luuid','-lcomctl32','-lgdi32']
    exe=output/'Ishar2-Cestina.exe'
    subprocess.run(args+['-o',str(exe)],check=True)
    subprocess.run(args+['-DISHAR_TESTING','-o',str(output/'installer-test.exe')],check=True)
    version=profile()['version'];dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    archive=dist/f'Ishar2-Cestina-{version}.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(exe,'Ishar2-Cestina.exe')
        z.writestr('CTI-ME.txt',(ROOT/'docs/CTI-ME.txt').read_text(encoding='utf-8').replace('{VERSION}',version).encode('utf-8-sig'))
        z.write(ROOT/'LICENSE','LICENSE-code.txt');z.write(ROOT/'LICENSING.md','LICENSING.md')
    (dist/'SHA256SUMS.txt').write_text(digest(archive.read_bytes())+'  '+archive.name+'\n',encoding='ascii')
    print('Release asset:',archive)

def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='action',required=True)
    commands.add_parser('check')
    for action in ('import','prepare','build'):
        cmd=commands.add_parser(action);cmd.add_argument('--game-dir',type=Path,required=True)
        if action=='build':cmd.add_argument('--cxx');cmd.add_argument('--windres')
    args=parser.parse_args()
    try:
        if args.action=='check':print('Validated',len(validate()[0]),'Czech units.')
        elif args.action=='import':context(args.game_dir)
        elif args.action=='prepare':prepare_payload(args.game_dir)
        else:build(args.game_dir,args.cxx,args.windres)
        return 0
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        print('ERROR:',error,file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
