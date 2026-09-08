"""Bounded regression checks for the website layer, not scientific revalidation."""
import ast
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]

def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename))
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module

build=load('bes_site_builder','build.py')
checks=load('bes_site_checks','check.py')
preview=load('bes_site_palette','preview_figures.py')

class WebsiteTests(unittest.TestCase):
    def test_inside_checkout_rejected(self):
        with self.assertRaises(ValueError):build.build(ROOT/'website/forbidden-output',None)
        self.assertFalse((ROOT/'website/forbidden-output').exists())

    def test_existing_destination_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises((ValueError,FileExistsError)):build.build(Path(folder),None)

    def test_baseline_contract(self):
        data=json.loads((ROOT/'website/scientific_baseline.json').read_text())
        self.assertEqual(data['commit'],'1059662eb7a8ad8bb3262ff4feddd9d95da71d00')
        self.assertEqual(len(data['files']),200)
        self.assertEqual(len({r['path'] for r in data['files']}),200)

    def test_color_literal_replacement_only(self):
        tree=ast.parse("a='#245b78'\nb=0.4\nc='science'\n")
        recolor=preview.Recolor({'#245b78':'#3F4D8C'})
        result=ast.literal_eval(recolor.visit(tree).body[0].value)
        self.assertEqual(result,'#3F4D8C');self.assertEqual(ast.literal_eval(tree.body[1].value),.4)
        self.assertEqual(ast.literal_eval(tree.body[2].value),'science');self.assertEqual(len(recolor.changed),1)

    def test_contrast_reference(self):
        self.assertAlmostEqual(checks.contrast('#000000','#FFFFFF'),21.)
        self.assertAlmostEqual(checks.contrast('#FFFFFF','#FFFFFF'),1.)

    def test_four_figure_contract(self):
        figures=json.loads((ROOT/'website/figures.json').read_text())
        self.assertEqual(len(figures),4);self.assertEqual(sum(len(x['panels']) for x in figures),6)
        for f in figures:
            for data in f['data']:self.assertTrue((ROOT/'data/processed/core_figures'/data).is_file())
            self.assertTrue((ROOT/'scripts/figures'/f['script']).is_file())

    def test_new_prose_no_em_dash(self):
        for p in (ROOT/'website/content').glob('*.md'):
            self.assertNotIn('\u2014',p.read_text(),str(p))

if __name__=='__main__':unittest.main()
