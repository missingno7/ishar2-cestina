"""Materialize editable PNGs locally; publish only changed pixel indices."""
from pathlib import Path
import argparse
import sys
from project import ROOT,load,save,originals

COLORS=[(0,0,0,0)]+[(70+i*12,)*3+(255,) for i in range(1,16)]
def values(data,glyph):
    start=glyph['offset'];size=glyph['width']*glyph['height']//2
    return [v for b in data[start:start+size] for v in (b>>4,b&15)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['export','import']);parser.add_argument('--game-dir',type=Path,required=True)
    args=parser.parse_args()
    try:
        from PIL import Image
        _,decoded=originals(args.game_dir);original=decoded['MAIN.IO']
        delta=load(ROOT/'translation/font-delta.json');directory=ROOT/'.local/font'
        paths={g['code']:directory/f'{g["code"]:02X}.png' for g in delta['glyphs']}
        if args.action=='export':
            if any(p.exists() for p in paths.values()):raise ValueError('PNG files already exist; preserve or move your local edits first')
            directory.mkdir(parents=True,exist_ok=True)
            for glyph in delta['glyphs']:
                pixels=values(original,glyph)
                for at,value in glyph['pixels']:pixels[at]=value
                image=Image.new('RGBA',(glyph['width'],glyph['height']));image.putdata([COLORS[p] for p in pixels])
                image.save(paths[glyph['code']])
            print('Exported',len(delta['glyphs']),'editable glyph PNGs to .local/font (do not publish).')
        else:
            lookup={v:i for i,v in enumerate(COLORS)}
            for glyph in delta['glyphs']:
                with Image.open(paths[glyph['code']]) as image:
                    if image.size!=(glyph['width'],glyph['height']):raise ValueError('Preserve glyph dimensions')
                    image=image.convert('RGBA')
                    colors=list(image.get_flattened_data() if hasattr(image,'get_flattened_data') else image.getdata())
                pixels=[]
                for color in colors:
                    if color[3]==0:pixels.append(0)
                    elif color in lookup:pixels.append(lookup[color])
                    else:raise ValueError('Unsupported color; use the existing palette without smoothing')
                glyph['pixels']=[[i,b] for i,(a,b) in enumerate(zip(values(original,glyph),pixels)) if a!=b]
            save(ROOT/'translation/font-delta.json',delta)
            print('Updated only pixel deltas in translation/font-delta.json.')
        return 0
    except ImportError:
        print('PNG editing requires Pillow: python -m pip install Pillow',file=sys.stderr);return 1
    except (ValueError,OSError,KeyError) as error:
        print('ERROR:',error,file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
