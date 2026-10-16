with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print('mobileMenuBtn present:', 'id="mobileMenuBtn"' in html)
print('mobileMenu present:', 'id="mobileMenu"' in html)
print('menuIconBurger present:', 'id="menuIconBurger"' in html)
print('menuIconClose present:', 'id="menuIconClose"' in html)
print('toggleMobileMenu count:', len(re.findall(r'function toggleMobileMenu', html)))
print('copilotWelcomeHint present:', 'id="copilotWelcomeHint"' in html)
