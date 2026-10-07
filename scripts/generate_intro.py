import xml.etree.ElementTree as ET
from svg import ROOT, command, save


def content(filename):
    root = ET.parse(ROOT / 'assets' / filename).getroot()
    return ''.join(ET.tostring(child, encoding='unicode') for child in root if child.tag.rsplit('}',1)[-1] not in ('title','style','rect'))


avatar = content('avatar.svg')
info = content('info-card.svg')
save('intro.svg',880,375,'CHIYO, Frontend Developer in Incheon. Original blue and white pixel cat. Founder of Pixel Hive Studio.',command('whoami') + f'<g transform="translate(0 85)">{avatar}</g><g transform="translate(330 65)">{info}</g>')
save('intro-mobile.svg',440,606,'CHIYO, Frontend Developer in Incheon. Original blue and white pixel cat. Founder of Pixel Hive Studio.',command('whoami') + f'<g transform="translate(65 60)">{avatar}</g><g transform="translate(0 301)">{info}</g>')
