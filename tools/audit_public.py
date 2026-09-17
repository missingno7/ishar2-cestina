"""Fail-closed source-tree audit; not a legal opinion or a license scanner."""
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','.local','build','dist','.venv','__pycache__','.pytest_cache'}
ROOT_FILES={'README.md','LICENSE','LICENSING.md','.gitignore','.gitattributes'}
EXTENSIONS={'src':{'.cpp','.rc','.manifest'},'tools':{'.py'},'tests':{'.py'},'docs':{'.md','.txt'},
    'translation':{'.json'},'metadata':{'.json'},'.github':{'.md','.yml'}}
DATA_FILES={'translation/cs.json','translation/glossary.json','translation/font-delta.json',
    'metadata/layout.json','metadata/profile.json'}

def verify(path):
    relative=path.relative_to(ROOT)
    if path.is_symlink():raise ValueError('Symlink is not a public source: '+str(relative))
    if relative.name=='patch_data.h':raise ValueError('Generated patch header must not be committed')
    if len(relative.parts)==1:
        if str(relative) not in ROOT_FILES:raise ValueError('Unreviewed root file: '+str(relative))
    elif path.suffix not in EXTENSIONS.get(relative.parts[0],set()):raise ValueError('Not an approved public source: '+str(relative))
    if relative.parts[0] in ('translation','metadata') and relative.as_posix() not in DATA_FILES:
        raise ValueError('Unreviewed data file: '+str(relative))
    data=path.read_bytes();text=data.decode('utf-8')
    if '\0' in text:raise ValueError('Binary content in source tree: '+str(relative))
    return len(data)

def audit():
    paths=[]
    def walk(directory):
        for path in directory.iterdir():
            if path.name in IGNORED:continue
            if path.is_symlink():raise ValueError('Symlink in source tree: '+str(path))
            if path.is_dir():walk(path)
            else:paths.append(path)
    walk(ROOT)
    total=sum(verify(p) for p in paths)
    # Gitignore is not enough: reject private/generated files already tracked.
    if (ROOT/'.git').exists():
        names=subprocess.check_output(['git','-c','safe.directory='+ROOT.as_posix(),'-C',str(ROOT),'ls-files','-z'])
        for name in names.decode('utf-8').split('\0'):
            if not name:continue
            rel=Path(name)
            if any(part in IGNORED for part in rel.parts):raise ValueError('Private/generated file tracked by Git: '+name)
            verify(ROOT/rel)
    layout=json.loads((ROOT/'metadata/layout.json').read_text(encoding='utf-8'))
    for unit in layout['units']:
        for ref in unit['english']+[r for rows in unit['references'].values() for r in rows]:
            if set(ref)!={'file','offset','length'}:raise ValueError('Reference must contain addresses only')
        for slot in unit['slots']:
            if 'raw' in slot or 'text' in slot:raise ValueError('Original text in public metadata')
    for row in json.loads((ROOT/'translation/cs.json').read_text(encoding='utf-8'))['units']:
        if set(row)!={'id','cs','status','lines'}:raise ValueError('Unreviewed translation fields')
    for term in json.loads((ROOT/'translation/glossary.json').read_text(encoding='utf-8'))['entries']:
        if 'en' in term:raise ValueError('Original-language glossary must stay private')
    print(f'Public source audit passed: {len(paths)} files, {total} bytes; private/build directories excluded.')
    return paths

if __name__=='__main__':
    try:audit()
    except (ValueError,OSError,subprocess.CalledProcessError) as error:print('ERROR:',error,file=sys.stderr);sys.exit(1)
