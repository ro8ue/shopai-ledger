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
            '/shopify-ai-support-apps', '/shopify-ai-search-apps', '/essays', '/stack-audit'])
        self.assertIn('>Subscribe</a>', home)
        self.assertNotIn("href='#support'", home)
        self.assertIn('shopify-ai-support-apps', self.read('sitemap.xml'))
        self.assertIn('shopify-ai-support-apps', self.read('sitemap.txt'))

    def test_ledger_uses_computed_medium_totals(self):
        data = json.loads((ROOT / 'data/apps.json').read_text())
        size = data['site']['sizes'][1]
        rate = data['site']['ai_rate']
        estimates = []
        for app in data['apps']:
            total = MODELS[app['model']](app['params'], size['conv'], size['seats'], int(size['conv'] * rate))['total']
            if total is not None:
                estimates.append((total, app['name'].split(' (')[0]))
        estimates.sort(key=lambda row: (row[0], row[1]))
        cheapest = estimates[:7]
        home = self.read('index.html')
        ledger = re.search(r'<aside class=ledger.*?<ol>(.*?)</ol>', home).group(1)
        rows = re.findall(r'<li>.*?</li>', ledger)
        self.assertEqual(len(rows), 7)
        self.assertIn('Cheapest seven support apps by medium-store cost', home)
        for row, (total, name) in zip(rows, cheapest):
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
            self.assertIn(f"href='/{app['slug']}-pricing'", support)

    def test_shared_assets_and_metadata(self):
        for path in (ROOT / 'site').glob('*.html'):
            text = path.read_text()
            if '<meta property="og:type"' not in text:  # Static 404 has no page() metadata.
                continue
            self.assertIn('Instrument+Sans', text)
            self.assertIn('Instrument+Serif:ital@0;1', text)
            og = re.search(r'<meta property="og:image" content="([^"]+)"', text)
            self.assertIsNotNone(og, path.name)
            self.assertTrue(
                og.group(1) == 'https://stillprice.com/og-default.jpg'
                or og.group(1).startswith('https://stillprice.com/essays-'),
                path.name)
            if og.group(1) == 'https://stillprice.com/og-default.jpg':
                self.assertIn('https://stillprice.com/og-default.jpg', text)
            else:
                self.assertIn(og.group(1), text)
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

    def test_clean_links_jsonld_and_placeholders(self):
        for path in (ROOT / 'site').glob('*.html'):
            text = path.read_text()
            self.assertIsNone(re.search(r"""href=['"](?!https?:)[^'"]*\.html""", text), path.name)
            self.assertNotIn('github.io', text)
            self.assertIsNone(re.search(r'<td[^>]*>\u2014</td>', text), path.name)
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
                json.loads(block)
        for name in ('shopify-ai-support-apps.html', 'shopify-ai-search-apps.html'):
            self.assertIn('"@type": "ItemList"', self.read(name))
        for name in ('gorgias-vs-tidio-pricing.html', 'doofinder-vs-algolia-pricing.html', 'gorgias-alternatives.html', 'klevu-alternatives.html'):
            self.assertIn('"@type": "BreadcrumbList"', self.read(name))
            self.assertIn('"dateModified"', self.read(name))
        self.assertNotIn('.html', self.read('sitemap.xml'))

    def test_homepage_subscribe_line(self):
        home = self.read('index.html')
        self.assertIn('hero-sub', home)
        self.assertIn('https://stillprice.substack.com/subscribe', home)
        self.assertIn('The Ledger, Mondays and Thursdays. Subscribe on Substack', home)

    def test_alternatives_affiliate_ctas(self):
        gorgias = self.read('gorgias-alternatives.html')
        self.assertIn("rel='sponsored noopener'", gorgias)
        self.assertIn('Try Gorgias (affiliate link)', gorgias)
        self.assertIn('affiliate status never changes a verdict', gorgias)
        searchanise = self.read('searchanise-alternatives.html')
        self.assertIn("rel='sponsored noopener'", searchanise)
        self.assertIn('Try Searchanise (affiliate link)', searchanise)
        self.assertIn('affiliate status never changes a verdict', searchanise)
        klevu = self.read('klevu-alternatives.html')
        self.assertNotIn('Try Klevu (affiliate link)', klevu)
        self.assertNotIn("rel='sponsored noopener'", klevu)

    def test_methodology_holds_email_sms(self):
        text = self.read('methodology.html')
        self.assertNotIn('id=emailsms', text)
        self.assertNotIn('Postscript', text)
        self.assertNotIn('2,500 contacts', text)
        self.assertTrue((ROOT / 'held' / 'methodology-email-sms-section.html').exists())

    def test_search_essay_uses_brent_header(self):
        text = self.read('essays-free-search-first-then-pay-by-product.html')
        self.assertIn("src='essays-free-search-first-then-pay-by-product-1456x816.png'", text)
        self.assertIn('https://stillprice.com/essays-free-search-first-then-pay-by-product-og-1200x630.png', text)
        self.assertIn('essay-hero-media', text)
        self.assertTrue((ROOT / 'site' / 'essays-free-search-first-then-pay-by-product-1456x816.png').exists())
        under = self.read('essays-ai-support-under-50-a-month.html')
        self.assertNotIn('essays-ai-support-under-50-a-month-1456x816.png', under)
        self.assertNotIn('essays-ai-support-under-50-a-month-og-1200x630.png', under)
        self.assertIn('https://stillprice.com/og-default.jpg', under)


if __name__ == '__main__':
    unittest.main()
