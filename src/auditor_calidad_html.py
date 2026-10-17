#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDE CIT — Auditoría Completa de Calidad del Portal HTML
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
"""
import sys, os, re
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "src" else Path(__file__).resolve().parent
PUBLIC = ROOT / "public" if (ROOT / "public").exists() else ROOT

HTML_FILES = {
    "index.html": PUBLIC / "index.html" if (PUBLIC / "index.html").exists() else ROOT / "index.html",
    "descargas-2017.html": PUBLIC / "descargas-2017.html" if (PUBLIC / "descargas-2017.html").exists() else ROOT / "descargas-2017.html",
    "guia-tecnica.html": PUBLIC / "guia-tecnica.html" if (PUBLIC / "guia-tecnica.html").exists() else ROOT / "guia-tecnica.html",
    "red-ides.html": PUBLIC / "red-ides.html" if (PUBLIC / "red-ides.html").exists() else ROOT / "red-ides.html",
    "ficha-mbht-2017.html": PUBLIC / "ficha-mbht-2017.html" if (PUBLIC / "ficha-mbht-2017.html").exists() else ROOT / "ficha-mbht-2017.html",
}

SECTION_SEP = "\n" + "=" * 80 + "\n"

class ImgAudit(HTMLParser):
    """Collect all <img> tags and check for alt, loading, width/height."""
    def __init__(self):
        super().__init__()
        self.imgs = []
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            d = dict(attrs)
            self.imgs.append(d)

class AnchorAudit(HTMLParser):
    """Collect all <a> tags."""
    def __init__(self):
        super().__init__()
        self.anchors = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            self.anchors.append(d)

class HeadingAudit(HTMLParser):
    """Collect heading hierarchy."""
    def __init__(self):
        super().__init__()
        self.headings = []
        self._current = None
    def handle_starttag(self, tag, attrs):
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self._current = tag
    def handle_endtag(self, tag):
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self._current = None
    def handle_data(self, data):
        if self._current:
            self.headings.append((self._current, data.strip()[:60]))
            self._current = None

def audit_file(name, path):
    print(SECTION_SEP)
    print(f"AUDITORÍA: {name}  ({path.stat().st_size // 1024} KB)")
    print("=" * 80)

    html = path.read_text(encoding="utf-8")
    issues = []
    warnings = []
    oks = []

    # -----------------------------------------------------------------------
    # 1. STRUCTURAL BASICS
    # -----------------------------------------------------------------------
    def chk(label, condition, is_warning=False):
        if condition:
            oks.append(label)
        else:
            (warnings if is_warning else issues).append(label)

    chk("DOCTYPE html5",              html.startswith("<!DOCTYPE html>"))
    chk("lang=es en <html>",          'lang="es"' in html)
    chk("charset=UTF-8",              'charset="UTF-8"' in html)
    chk("<meta name=viewport>",       'name="viewport"' in html)
    chk("<title> presente",           "<title>" in html)
    chk("meta description",           'name="description"' in html)
    chk("meta keywords",              'name="keywords"' in html)
    chk("meta author",                'name="author"' in html)
    chk("canonical link",             'rel="canonical"' in html)
    chk("Open Graph og:title",        'property="og:title"' in html)
    chk("Open Graph og:description",  'property="og:description"' in html)
    chk("Open Graph og:image",        'property="og:image"' in html)
    chk("Open Graph og:url",          'property="og:url"' in html)
    chk("Twitter card",               'name="twitter:card"' in html)
    chk("JSON-LD Schema.org",         'application/ld+json' in html)
    chk("webmanifest link",           'site.webmanifest' in html, is_warning=True)
    chk("theme-color meta",           'name="theme-color"' in html, is_warning=True)
    chk("preconnect hint",            'rel="preconnect"' in html, is_warning=True)
    chk("noscript fallback",          "<noscript" in html, is_warning=True)

    # -----------------------------------------------------------------------
    # 2. ACCESSIBILITY
    # -----------------------------------------------------------------------
    chk("aria-label present",         'aria-label' in html)
    chk("role= attributes",           'role=' in html)
    chk("tabindex for focusable",     'tabindex=' in html)
    chk("focus-visible / focus:ring", 'focus:ring' in html or 'focus-visible' in html)
    chk("skip-to-main-content",       'skip' in html.lower() and 'main' in html.lower(), is_warning=True)
    chk("sr-only screen reader text", 'sr-only' in html, is_warning=True)
    chk("button type= defined",       'type="button"' in html)
    chk("input type= defined",        'type="text"' in html or 'type="search"' in html, is_warning=True)

    # -----------------------------------------------------------------------
    # 3. IMAGES
    # -----------------------------------------------------------------------
    img_parser = ImgAudit()
    img_parser.feed(html)
    imgs_no_alt = [i for i in img_parser.imgs if not i.get("alt") and i.get("alt") != ""]
    imgs_no_lazy = [i for i in img_parser.imgs if i.get("loading") != "lazy"]

    if imgs_no_alt:
        issues.append(f"<img> sin alt: {len(imgs_no_alt)} imágenes")
    else:
        oks.append(f"Todas las <img> tienen alt ({len(img_parser.imgs)} imágenes)")

    if imgs_no_lazy and len(imgs_no_lazy) > 3:
        warnings.append(f"<img> sin loading=lazy: {len(imgs_no_lazy)}")
    else:
        oks.append("loading=lazy en imágenes (o sin imágenes)")

    # -----------------------------------------------------------------------
    # 4. LINKS
    # -----------------------------------------------------------------------
    anchor_parser = AnchorAudit()
    anchor_parser.feed(html)
    ext_links_no_rel = [a for a in anchor_parser.anchors
                        if a.get("href", "").startswith("http")
                        and "noopener" not in a.get("rel", "")]
    if ext_links_no_rel:
        warnings.append(f"Links externos sin rel=noopener: {len(ext_links_no_rel)}")
    else:
        oks.append("Links externos con rel=noopener noreferrer")

    broken_hash_links = [a for a in anchor_parser.anchors
                         if a.get("href", "").startswith("#")
                         and a["href"] != "#"
                         and a["href"][1:] not in html]
    if broken_hash_links:
        warnings.append(f"Links internos (#anchor) potencialmente rotos: {len(broken_hash_links)}")

    # -----------------------------------------------------------------------
    # 5. HEADING HIERARCHY
    # -----------------------------------------------------------------------
    h_parser = HeadingAudit()
    h_parser.feed(html)
    h_tags = [h[0] for h in h_parser.headings]
    has_h1 = "h1" in h_tags
    multi_h1 = h_tags.count("h1") > 1
    chk("Un solo <h1>",  has_h1 and not multi_h1)
    if multi_h1:
        issues.append(f"Múltiples <h1> encontrados: {h_tags.count('h1')}")

    # -----------------------------------------------------------------------
    # 6. JAVASCRIPT QUALITY
    # -----------------------------------------------------------------------
    chk("console.log removido",  'console.log' not in html, is_warning=True)
    chk("console.error en prod", 'console.error' not in html, is_warning=True)
    chk("addEventListener vs inline onclick",
        html.count(' onclick=') < 5, is_warning=True)
    chk("defer/async en scripts externos",
        'defer' in html or 'async' in html, is_warning=True)

    # -----------------------------------------------------------------------
    # 7. PERFORMANCE
    # -----------------------------------------------------------------------
    chk("Tailwind CDN (no ideal prod)", 'cdn.tailwindcss' not in html, is_warning=True)
    inline_style_count = html.count(' style="')
    if inline_style_count > 50:
        warnings.append(f"Muchos style= inline: {inline_style_count}")
    else:
        oks.append(f"Estilos inline razonables ({inline_style_count})")

    # -----------------------------------------------------------------------
    # 8. SECURITY
    # -----------------------------------------------------------------------
    chk("Sin target=_blank sin noopener",
        'target="_blank"' not in html or 'noopener' in html)
    chk("innerHTML con innerHTML=",
        html.count('innerHTML') < 30, is_warning=True)

    # -----------------------------------------------------------------------
    # 9. DOWNLOAD LINKS CONSISTENCY
    # -----------------------------------------------------------------------
    import re
    download_links = re.findall(r'href=["\']download/([^"\']+)["\']', html)
    missing_dl = []
    dl_dir = ROOT / "download"
    for link in download_links:
        if not (dl_dir / link).exists():
            missing_dl.append(link)
    if missing_dl:
        issues.append(f"Download links rotos ({len(missing_dl)}): {missing_dl[:3]}")
    elif download_links:
        oks.append(f"Download links verificados: {len(download_links)} links OK")

    # -----------------------------------------------------------------------
    # REPORT
    # -----------------------------------------------------------------------
    print(f"\n  ✅ OK ({len(oks)}):")
    for o in oks:
        print(f"     ✓ {o}")

    if warnings:
        print(f"\n  ⚠️  ADVERTENCIAS ({len(warnings)}):")
        for w in warnings:
            print(f"     ⚠ {w}")

    if issues:
        print(f"\n  ❌ PROBLEMAS CRÍTICOS ({len(issues)}):")
        for i in issues:
            print(f"     ✗ {i}")
    else:
        print(f"\n  🎉 SIN PROBLEMAS CRÍTICOS")

    # Heading hierarchy
    print(f"\n  📐 Jerarquía de encabezados ({len(h_parser.headings)} total):")
    for tag, text in h_parser.headings[:15]:
        print(f"     <{tag}> {text}")
    if len(h_parser.headings) > 15:
        print(f"     ... ({len(h_parser.headings) - 15} más)")

    score = len(oks) / (len(oks) + len(issues)) * 100 if (oks or issues) else 100
    print(f"\n  PUNTUACIÓN: {score:.1f}% ({len(oks)} OK, {len(warnings)} advertencias, {len(issues)} críticos)")

    return {"file": name, "oks": len(oks), "warnings": len(warnings), "issues": issues, "score": score}

if __name__ == "__main__":
    results = []
    for name, path in HTML_FILES.items():
        if path.exists():
            r = audit_file(name, path)
            results.append(r)
        else:
            print(f"\n  ⚠️ Archivo no encontrado: {path}")

    print(SECTION_SEP)
    print("RESUMEN CONSOLIDADO DE AUDITORÍA — IDE CIT")
    print("=" * 80)
    for r in results:
        print(f"  {r['file']}: {r['score']:.1f}% — {r['oks']} OK, {r['warnings']} advertencias, {len(r['issues'])} críticos")
    avg = sum(r['score'] for r in results) / len(results) if results else 0
    print(f"\n  PUNTUACIÓN GLOBAL: {avg:.1f}%")
    all_issues = [i for r in results for i in r['issues']]
    if all_issues:
        print(f"\n  ⚡ ACCIONES PRIORITARIAS:")
        for issue in all_issues:
            print(f"     → {issue}")
    else:
        print("\n  🏆 PORTAL IDE CIT: CALIDAD DE EXCELENCIA VERIFICADA")
