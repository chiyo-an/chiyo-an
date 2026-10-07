import json
import unittest
from pathlib import Path
from unittest.mock import patch
import xml.etree.ElementTree as ET
from fetch_contributions import parse_calendar, main
from generate_contribution import render
from svg import ROOT


class ProfileTests(unittest.TestCase):
    def test_real_data_and_grid(self):
        payload = json.loads((ROOT / 'data/contributions.json').read_text())
        render(payload)
        tree = ET.parse(ROOT / 'assets/contribution.svg')
        cells = [node for node in tree.iter('{http://www.w3.org/2000/svg}rect') if node.find('{http://www.w3.org/2000/svg}title') is not None]
        self.assertEqual(len(cells), 53*7)
        self.assertGreaterEqual(len(payload['days']),365)

    def test_changed_html_is_rejected(self):
        for html in ['', '<html>Sign in</html>', '<td data-date="2026-01-01" data-level="9"></td>']:
            with self.assertRaises(ValueError):
                parse_calendar(html)

    def test_failure_preserves_data(self):
        path = ROOT / 'data/contributions.json'
        original = path.read_bytes()
        with patch('fetch_contributions.fetch', side_effect=ValueError('changed HTML')), patch('sys.argv',['fetch']):
            self.assertEqual(main(),1)
        self.assertEqual(path.read_bytes(),original)

    def test_empty_state(self):
        with patch('generate_contribution.save') as save:
            render({'username':'chiyo-an','days':[]})
            self.assertIn('data unavailable',save.call_args.args[3])

    def test_svg_and_readme_paths(self):
        import re
        for path in (ROOT / 'assets').glob('*.svg'):
            root = ET.parse(path).getroot()
            self.assertIn('viewBox',root.attrib)
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
            self.assertNotIn('<script',path.read_text())
        for name in re.findall(r'\./(assets/[^" ]+)',(ROOT/'README.md').read_text()):
            self.assertTrue((ROOT/name).is_file(),name)


if __name__ == '__main__':
    unittest.main()
