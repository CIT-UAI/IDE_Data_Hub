from pathlib import Path
import re

root = Path('.')
html_files = ['index.html', 'descargas-2017.html', 'guia-tecnica.html', 'red-ides.html']

for h in html_files:
    txt = (root / h).read_text(encoding='utf-8')
    has_btn = 'id="btnScrollTop"' in txt
    num_scroll_to_top = len(re.findall(r'scrollToTop', txt))
    num_check_scroll = len(re.findall(r'updateScrollBtn', txt))
    print(f'{h}: btnScrollTop={has_btn}, scrollToTop refs={num_scroll_to_top}, updateScrollBtn refs={num_check_scroll}')

cat = (root / 'data' / 'catalogo_ide_cit.json').read_text(encoding='utf-8')
red = (root / 'red-ides.html').read_text(encoding='utf-8')

for name, url in [('Visor Territorial', 'https://miratuterritorio.ide.cl/'), ('Observatorio Urbano', 'https://calidaddevida.minvu.gob.cl/'), ('SUBPESCA', 'https://mapas.subpesca.cl/ideviewer/')]:
    in_cat = url in cat
    in_red = url in red
    print(f'{name} ({url}): in json={in_cat}, in red-ides={in_red}')

for bad in ['visorterritorial.cl', 'observatoriourbano.cl', 'cebiclar', 'lagatahoracia']:
    print(f'Bad keyword "{bad}" in red-ides: {bad in red}, in catalogo: {bad in cat}')
