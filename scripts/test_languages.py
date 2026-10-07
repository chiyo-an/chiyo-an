import unittest
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
from generate_languages import parse, render
from svg import ROOT


class LanguageTests(unittest.TestCase):
    def test_original_values_preserved(self):
        languages=parse(ROOT/'metrics.svg')
        self.assertEqual(dict(languages)['JavaScript'],38.24)
        self.assertEqual(dict(languages)['TypeScript'],5)
        self.assertEqual(len(languages),8)
        for mobile in [False,True]:
            render(languages,mobile)
            ET.parse(ROOT/'assets'/('languages-mobile.svg' if mobile else 'languages.svg'))

    def test_missing_data_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'empty.svg';p.write_text('<svg/>')
            with self.assertRaises(ValueError):parse(p)

    def test_readme_paths(self):
        import re
        for name in re.findall(r'\./(assets/[^" ]+)',(ROOT/'README.md').read_text()):
            self.assertTrue((ROOT/name).is_file())
        self.assertNotIn('contribution.svg',(ROOT/'README.md').read_text())


if __name__=='__main__':unittest.main()
