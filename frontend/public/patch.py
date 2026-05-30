import glob
import os

for file in glob.glob('*.html'):
    if file in ['index.html', 'login.html', 'register.html', 'analyze.html', 'profile.html', 'recruiter.html']: continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/js/auth.js' not in content:
        inject = '<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>\n<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>\n<script src="/js/auth.js"></script>\n<script src="/js/pages/auth-shared.js"></script>\n<script src="/js/config.js"></script>'
        content = content.replace('<script src="/js/config.js"></script>', inject)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched {file}')
