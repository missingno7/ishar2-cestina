"""Unicode -> existing Ishar glyph slots. No font expansion or EXE patch."""
import unicodedata
CS={'á': 47, 'é': 91, 'č': 35, 'ň': 37, 'ř': 38, 'š': 42, 'ť': 60, 'ý': 61, 'ě': 62, 'ž': 92, 'ó': 93, 'í': 95, 'ů': 96, 'ď': 123, 'ú': 125, 'Č': 36, 'Ž': 94}
LITERAL='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:\'"()+-'

UPPER='ÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ'
FALLBACK={ch:base for ch,base in zip(UPPER,'ACDEEINORSTUUYZ') if ch not in CS}
FALLBACK.update({'Ú':'ú','Š':'š'})
TYPOGRAPHY={'’':"'",'‘':"'",'“':'"','”':'"','„':'"','–':'-','—':'-','…':'...', '\u00a0':' '}

def encode(text):
    if not isinstance(text,str):raise ValueError('Text must be a string')
    text=unicodedata.normalize('NFC',text)
    out=bytearray();rendered=[];changes=[]
    for ch in text:
        replacement=FALLBACK.get(ch,TYPOGRAPHY.get(ch,ch))
        if replacement!=ch:changes.append({'from':ch,'to':replacement})
        for c in replacement:
            if c in CS:out.append(CS[c])
            elif c in LITERAL:out.append(ord(c))
            else:raise ValueError(f'Unsupported game character {c!r}')
            rendered.append(c)
            if 'A'<=c<='Z' or c in UPPER:out.append(32)  # keep 12 px advance for every capital
    return bytes(out),''.join(rendered),changes

def slot_bytes(text,slot):
    # Alignment padding belongs to the compiler, never to the clean translation.
    payload,visible,changes=encode(text.strip(' '))
    payload=b' '*slot['leading_spaces']+payload
    required=len(payload)+slot['trailing_spaces']
    if required>slot['max_bytes']:
        raise ValueError(f'{required} B exceeds {slot["max_bytes"]} B (including capital spacing/alignment)')
    return payload.ljust(slot['max_bytes'],b' '),dict(
        used_bytes=required,max_bytes=slot['max_bytes'],spare_bytes=slot['max_bytes']-required,
        visible=visible,substitutions=changes)
