"""Bounded-run A1 encoder for large Silmarils resources.

Uses the existing decoded resource layout unchanged. This standalone build
needs no original executable dump; Python and C++ implementations are checked
against the reference release output. No 16-bit literal count may overflow.
"""
from collections import defaultdict,deque

def unpack(data):
    """Bounded A1 decoder, independent of the original executable.

    Old streams may read beyond their physical end. At most 16 bytes of zero
    lookahead are permitted. Native tail corrections belong to the profile.
    """
    if len(data)<6:raise ValueError('Short resource header')
    declared=int.from_bytes(data[:3],'little')
    header=22 if data[4:6]==b'\0\0' else 6
    if not header<=declared<=2*1024*1024:raise ValueError('Invalid declared length')
    if not data[3]&128:
        if len(data)!=declared:raise ValueError('Invalid uncompressed length')
        return data
    if data[3]!=0xa1 or len(data)<header+8:raise ValueError('Unsupported compression')
    widths=data[header:header+8]
    if any(n>16 for n in widths):raise ValueError('Invalid distance width')
    at=(header+8)*8
    def bits(n):
        nonlocal at
        if at+n>(len(data)+16)*8:raise ValueError('Truncated compressed stream')
        result=0
        for _ in range(n):
            result=(result<<1)|((data[at//8]>>(7-at%8))&1 if at//8<len(data) else 0)
            at+=1
        return result
    def count(initial,width):
        total=initial
        while True:
            n=bits(width);total+=n
            if total>65535:raise ValueError('Token exceeds 16-bit limit')
            if n!=(1<<width)-1:return total
    out=bytearray(data[:header])
    while len(out)<declared:
        if bits(1):
            for _ in range(min(count(1,2),declared-len(out))):out.append(bits(8))
            if len(out)==declared:break
        mode=bits(3);distance=bits(widths[mode])+1
        length=count(5,3) if mode%4==0 else mode%4+1
        if distance>len(out)-header:raise ValueError('Reference before payload')
        for _ in range(min(length,declared-len(out))):out.append(out[-distance])
    return bytes(out)

WIDTHS=(11,9,10,11,7,5,6,7)

def pack_a1(raw):
    header=22 if raw[4:6]==b'\0\0' else 6
    if len(raw)<header or int.from_bytes(raw[:3],'little')!=len(raw):
        raise ValueError('A1 input must have its exact declared decoded length')
    src=raw[header:]
    if not src:raise ValueError('Empty A1 resource')
    out=bytearray(raw[:header]);out[3]=0xa1;out.extend(WIDTHS)
    acc=0;nbits=0
    def put(value,n):
        nonlocal acc,nbits
        assert 0<=value<(1<<n)
        acc=(acc<<n)|value;nbits+=n
        while nbits>=8:
            nbits-=8;out.append((acc>>nbits)&255)
            acc&=(1<<nbits)-1
    def groups(count,bits):
        limit=(1<<bits)-1
        while count>=limit:put(limit,bits);count-=limit
        put(count,bits)
    history=defaultdict(lambda:deque(maxlen=64))
    def remember(pos):
        if pos+1<len(src):history[src[pos:pos+2]].append(pos)
    def match(pos):
        if pos+1>=len(src):return None
        best=None;gain=0
        for prev in reversed(history.get(src[pos:pos+2],())):
            distance=pos-prev
            if distance>2048:break
            count=2;limit=min(512,len(src)-pos)
            while count<limit and src[prev+count]==src[pos+count]:count+=1
            for mode,width in enumerate(WIDTHS):
                if distance>1<<width:continue
                length=count if mode%4==0 else mode%4+1
                if length>count or (mode%4==0 and count<5):continue
                cost=3+width+(3*((length-5)//7+1) if mode%4==0 else 0)
                saving=8*length-cost
                if saving>gain:best=(mode,distance,length);gain=saving
        return best
    pos=0
    while pos<len(src):
        begin=pos;found=match(pos)
        while pos<len(src) and found is None:
            remember(pos);pos+=1
            found=match(pos) if pos<len(src) else None
        count=pos-begin
        if count>65535:raise ValueError('A1 literal run exceeds original 16-bit decoder capacity')
        put(bool(count),1)
        if count:
            groups(count-1,2)
            for byte in src[begin:pos]:put(byte,8)
        if pos==len(src):break
        mode,distance,length=found
        put(mode,3);put(distance-1,WIDTHS[mode])
        if mode%4==0:groups(length-5,3)
        for at in range(pos,pos+length):remember(at)
        pos+=length
    if nbits:out.append(acc<<(8-nbits))
    out.extend(b'\0\0\0\0') # original bit-reader prefetch, outside decoded length
    return bytes(out)
