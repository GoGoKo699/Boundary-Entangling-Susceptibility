#!/usr/bin/env python3
"""Capture the generated site for in-repository review without hosting it.

Local CSS, scripts and images are inlined; all browser network requests are
blocked. These are layout screenshots, not tests of live deployment.
"""
from __future__ import annotations
import argparse
import base64
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def document(site: Path, source: Path) -> str:
    soup = BeautifulSoup(source.read_text(), 'html.parser')
    def local(url: str) -> Path:
        bits = urlsplit(url)
        if bits.scheme or bits.netloc:
            raise ValueError(f'External runtime resource refused: {url}')
        path = (source.parent / unquote(bits.path)).resolve()
        if not path.is_relative_to(site):
            raise ValueError('Asset outside the built site')
        return path
    for link in soup.find_all('link', rel='stylesheet'):
        style = soup.new_tag('style')
        style.string = local(link['href']).read_text()
        link.replace_with(style)
    for script in soup.find_all('script', src=True):
        text = local(script['src']).read_text()
        del script['src']
        script.attrs.pop('defer', None)
        script.string = text
        # Run after body exists, as the original deferred script would.
        script.extract()
        soup.body.append(script)
    for image in soup.find_all('img', src=True):
        path = local(image['src'])
        mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        image['src'] = f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()
        image.attrs.pop('loading', None)
    return str(soup)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--browser-executable', type=str, help='Optional existing Chromium binary')
    args = parser.parse_args()
    site = args.site.resolve()
    if not (site / 'BUILD.json').is_file():
        raise ValueError('Expected a validated generated website')
    args.output.mkdir(parents=True, exist_ok=True)
    cases = [('index.html', 1440, 1000, 'home-desktop.png'),
             ('index.html', 390, 844, 'home-mobile.png'),
             ('design/index.html', 1440, 1000, 'palette-desktop.png')]
    records = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**({'executable_path': args.browser_executable} if args.browser_executable else {}))
        for source, width, height, name in cases:
            page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
            page.route('**/*', lambda route: route.abort())
            page.set_content(document(site, site/source), wait_until='load')
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(200)
            overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
            if overflow:
                raise AssertionError(f'Page-level horizontal overflow: {name}')
            page.screenshot(path=str(args.output/name), full_page=True)
            records.append({'page': source, 'width': width, 'screenshot': name, 'page_overflow': overflow})
            page.close()
        browser.close()
    (args.output/'capture.json').write_text(json.dumps({
        'scope': 'In-memory rendering of the built local HTML; not live hosting',
        'network_blocked': True, 'screenshots': records}, indent=2)+'\n')


if __name__ == '__main__':
    main()
