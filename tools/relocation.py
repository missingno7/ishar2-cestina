"""Relocate explicitly approved VM literal assignments; no original assets here."""
import hashlib
from text_codec import slot_bytes

def jump(start,target):
    delta=target-(start+4)
    if not -32768<=delta<=32767:raise ValueError('Relocation jump outside supported range')
    return b'\x0a'+(delta&65535).to_bytes(2,'little')+bytes([255 if delta<0 else 0])

def relocate(raw,slot,text):
    rule=slot['relocation'];start=rule['start'];resume=rule['resume'];offset=slot['offset']
    end=offset+slot['max_bytes']
    if start!=offset-2 or not 0<=start<end<resume<=len(raw):raise ValueError('Invalid relocation boundaries')
    original=bytes(raw[start:resume])
    if hashlib.sha256(original).hexdigest()!=rule['instruction_sha256']:raise ValueError('Original instruction mismatch')
    if bytes(raw[start:offset])!=b'\x1e\x04' or raw[end]!=0:raise ValueError('Not a literal assignment')
    suffix=bytes(raw[end:resume])
    if not ((len(suffix)==3 and suffix[1]==0x16) or
            (len(suffix)==4 and suffix[1]==0x0a) or
            (len(suffix)==7 and suffix[1:6]==b'\x38\x00\x00\x3a\x18')):
        raise ValueError('Unsupported assignment destination')
    if not text or b'\0' in text or len(text)>rule['max_bytes']:raise ValueError('Invalid relocated text')
    trailer=len(raw);block=b'\x1e\x04'+text+suffix
    if trailer+len(block)+4>=65536:raise ValueError('Relocated resource exceeds supported segment')
    forward=jump(start,trailer);backward=jump(trailer+len(block),resume)
    # Preserve the unreachable Czech bytes from the approved test build.
    retained=slot_bytes(rule['retained_cs'],slot)[0]
    raw[offset:end]=retained
    raw[start:start+4]=forward
    raw.extend(block+backward)
    raw[:3]=len(raw).to_bytes(3,'little')
