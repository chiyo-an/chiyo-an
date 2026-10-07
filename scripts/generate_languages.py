import argparse
import math
from pathlib import Path
import xml.etree.ElementTree as ET
from svg import GRAY, ROOT, command, save, text


def parse(source):
    root = ET.parse(source).getroot()
    ns = {'h':'http://www.w3.org/1999/xhtml'}
    languages = []
    for node in root.findall('.//h:div', ns):
        if 'language' not in node.attrib.get('class','').split() or 'details' not in node.attrib.get('class','').split():
            continue
        field = node.find('h:div',ns)
        percent = node.find('h:small/h:div',ns)
        if field is None or percent is None:
            raise ValueError('Metrics language structure changed')
        name = ''.join(field.itertext()).strip()
        value = float(percent.text.strip().removesuffix('%'))
        if not name or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError('Invalid language data')
        languages.append((name,value))
    if not languages or len({name for name,_ in languages}) != len(languages) or sum(value for _,value in languages)>100.1:
        raise ValueError('Missing or inconsistent metrics language data')
    return sorted(languages,key=lambda item:item[1],reverse=True)


def render(languages, mobile=False):
    width = 440 if mobile else 880
    parts = command('cat ./languages')
    parts += text(28,85,'Repository language distribution',14,GRAY)
    colors = ['#a9d8f5','#93c8e9','#7db4db','#689fcb','#568bb8','#4577a4','#37648d','#2c5275']
    for i,(name,value) in enumerate(languages):
        y=121+i*28
        parts += text(28,y,name,14)+text(width-28,y,f'{value:g}%',14,GRAY,'text-anchor="end"')
        x=152 if mobile else 220
        span=width-x-105
        parts += f'<rect x="{x}" y="{y-10}" width="{span}" height="6" rx="3" fill="#20252d"/>'
        parts += f'<rect x="{x}" y="{y-10}" width="{span*value/100:.3f}" height="6" rx="3" fill="{colors[i%len(colors)]}"/>'
    footer=121+len(languages)*28+14
    parts+=text(28,footer,'Code distribution, not proficiency.',12,GRAY)
    title='Repository language distribution: '+', '.join(f'{name} {value:g}%' for name,value in languages)
    save('languages-mobile.svg' if mobile else 'languages.svg',width,footer+32,title,parts)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=ROOT/'metrics.svg')
    languages=parse(parser.parse_args().source)
    render(languages)
    render(languages,True)
