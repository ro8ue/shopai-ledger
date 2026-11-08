"""Regression checks for the static editorial design. Run: python3 -m unittest discover -s tests."""
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calc import MODELS, m


class ComparisonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.comparison = False
        self.costs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table':
            self.comparison = attrs.get('class') == 'cmp'
        if self.comparison and tag == 'td' and 'data-size' in attrs:
            self.costs.append(attrs['data-size'])

    def handle_endtag(self, tag):
        if tag == 'table':
            self.comparison = False


class DesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True)

    def read(self, name):
        return (ROOT / 'site' / name).read_text()

    def test_cover_and_navigation(self):
        home = self.read('index.html')
        self.assertNotIn('class=cmp', home)
        nav = re.search(r'<nav class="main"[^>]*>(.*?)</nav>', home).group(1)
        self.assertEqual(re.findall(r'href="([^"]+)"', nav), [
            'shopify-ai-support-apps.html', 'shopify-ai-search-apps.html', 'essays.html', '/stack-audit'])
        self.assertIn('>Subscribe</a>', home)
        self.assertNotIn("href='#support'", home)
        self.assertIn('shopify-ai-support-apps', self.read('sitemap.xml'))
        self.assertIn('shopify-ai-support-apps', self.read('sitemap.txt'))

    def test_ledger_uses_computed_medium_totals(self):
        data = json.loads((ROOT / 'data/apps.json').read_text())
        size = data['site']['sizes'][1]
        rate = data['site']['ai_rate']
        wanted = {'shopify-inbox', 'aide', 'helpcenter', 'chatty', 'zipchat', 'gorgias', 'zendesk'}
        estimates = []
        for app in data['apps']:
            if app['slug'] in wanted:
                total = MODELS[app['model']](app['params'], size['conv'], size['seats'], int(size['conv'] * rate))['total']
                estimates.append((total, app['name'].split(' (')[0]))
        ledger = re.search(r'<aside class=ledger.*?<ol>(.*?)</ol>', self.read('index.html')).group(1)
        rows = re.findall(r'<li>.*?</li>', ledger)
        self.assertEqual(len(rows), len(wanted))
        for row, (total, name) in zip(rows, sorted(estimates)):
            self.assertIn(html.escape(name), row)
            self.assertIn(f'<b>{m(total)}</b>', row)

    def test_comparisons_preserve_every_size(self):
        for filename in ('shopify-ai-support-apps.html', 'shopify-ai-search-apps.html',
                         'gorgias-alternatives.html', 'klevu-alternatives.html', 'boost-ai-search-alternatives.html'):
            text = self.read(filename)
            self.assertIn("data-selected-size='medium'", text)
            self.assertIn("role='group' aria-label='Store size'", text)
            parser = ComparisonParser()
            parser.feed(text)
            self.assertTrue(parser.costs)
            self.assertEqual(parser.costs, ['small', 'medium', 'large'] * (len(parser.costs) // 3))
            self.assertNotIn('Swipe sideways', text)
        # Every support app, including unpublished prices, remains in the full category.
        data = json.loads((ROOT / 'data/apps.json').read_text())
        support = self.read('shopify-ai-support-apps.html')
        for app in data['apps']:
            self.assertIn(f"href='{app['slug']}-pricing.html'", support)

    def test_shared_assets_and_metadata(self):
        for path in (ROOT / 'site').glob('*.html'):
            text = path.read_text()
            if '<meta property="og:type"' not in text:  # Static 404 has no page() metadata.
                continue
            self.assertIn('Instrument+Sans', text)
            self.assertIn('Instrument+Serif:ital@0;1', text)
            self.assertIn('https://stillprice.com/og-default.jpg', text)
            self.assertIn('summary_large_image', text)
            self.assertIn('src="table-sizes.js"', text)
        for asset in ('og-default.jpg', 'table-sizes.js'):
            self.assertEqual((ROOT / 'assets' / asset).read_bytes(), (ROOT / 'site' / asset).read_bytes())
        css = self.read('style.css')
        for old in ('Cormorant', 'Geist', 'Inter,', 'scale(1.03)', 'border-radius:999px'):
            self.assertNotIn(old, css)

    def test_audit_offer_and_form_preserved(self):
        text = self.read('stack-audit.html')
        self.assertIn('$149', text)
        self.assertIn('Fee waived for these first requests.', text)
        source = (ROOT / 'templates/stack-audit.html').read_text()
        form = re.search(r'<form.*?</form>', source, re.S).group(0)
        self.assertIn(form, text)
        self.assertIn('border-radius:var(--r)', self.read('stack-audit.css'))


if __name__ == '__main__':
    unittest.main()
